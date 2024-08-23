import http.client
import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime
from sqlalchemy import func

# Import các model và cấu hình 
from .model import db, tbt_detail_stock_price
from api.session.model import tbt_session
from api.stock.model import tbt_stock
from api.config import DETAIL_CAFEF_URL, DETAIL_CAFEF_REFERER_URL, DETAIL_CAFEF_STATISTICAL_URL

# Hàm lấy stock_id từ bảng tbt_stock
def get_stock_id(symbol):
    stock = tbt_stock.query.filter_by(code=symbol).first()
    return (stock.id, stock.stock_space) if stock else None

# Hàm lấy session_id từ bảng session dựa vào ngày và stock_space
def get_session_id(date_str, stock_space):
    if not date_str:
        return None

    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError as e:
        return None

    session_obj = tbt_session.query.filter_by(
        year=date.year, month=date.month, day_of_month=date.day, stock_space=stock_space
    ).first()
    return session_obj.id if session_obj else None

# Hàm lấy tất cả mã chứng khoán từ bảng tbt_stock
def get_all_symbols():
    stocks = tbt_stock.query.with_entities(tbt_stock.code).all()
    return [stock.code for stock in stocks]

# Hàm chèn dữ liệu vào bảng detail_stock_price
def insert_into_db(data):
    db.session.bulk_insert_mappings(tbt_detail_stock_price, data)
    db.session.commit()

# Hàm lấy ngày mới nhất có dữ liệu từ sql
def get_latest_date(stock_id):
    latest_date = db.session.query(
        func.max(
            func.concat(
                tbt_session.year,
                '-',
                func.lpad(tbt_session.month, 2, '0'),
                '-',
                func.lpad(tbt_session.day_of_month, 2, '0')
                        )
                ).label('latest_date')
    ).select_from(tbt_detail_stock_price).join(
        tbt_session,
        tbt_detail_stock_price.session_id == tbt_session.id
    ).filter(
        tbt_detail_stock_price.stock_id == stock_id,
    ).scalar()

    # if latest_date:
    #     latest_date = datetime.strptime(latest_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    return latest_date

# Hàm lấy dữ liệu từ api detail
def fetch_detail_data(symbol, page_number, start_date=None, end_date=None):
    conn = http.client.HTTPSConnection("s.cafef.vn")
    headers = {"Referer": DETAIL_CAFEF_REFERER_URL}
    url = DETAIL_CAFEF_URL.format(symbol=symbol, page_number=page_number, start_date=start_date, end_date=end_date)
    conn.request("GET", url, "", headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data

# Hàm lấy dữ liệu từ api statistical
def fetch_statistical_data(symbol, page_number, start_date=None, end_date=None):
    conn = http.client.HTTPSConnection("s.cafef.vn")
    headers = {"Referer": DETAIL_CAFEF_REFERER_URL}
    url = DETAIL_CAFEF_STATISTICAL_URL.format(symbol=symbol, page_number=page_number, start_date=start_date, end_date=end_date)
    conn.request("GET", url, "", headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data

def fetch_detail_stock_data():
    symbols = get_all_symbols()
    for symbol in symbols:
        stock_info = get_stock_id(symbol)
        if stock_info is None:
            print(f"No stock_id found for {symbol}")
            continue

        stock_id, stock_space = stock_info
        all_data = []
        # Lấy date mới nhất từ CSDL
        latest_date = get_latest_date(stock_id)
        if latest_date:
            start_date = latest_date
            print(f"Updating data from {start_date} for {symbol}")
        else:
            start_date = datetime.min.strftime("%d/%m/%Y")
            print(f"No existing data found, fetching all data for {symbol}")
        
        end_date = datetime.now().strftime("%d/%m/%Y")

        # Fetch detail data
        page_number = 1
        while True:
            data = fetch_detail_data(symbol, page_number, start_date, end_date)
            if not data:
                break
            try:
                json_data = json.loads(data)
                if not json_data.get('Data'):
                    break
                df_detail = json_normalize(json_data['Data'], record_path='Data')
                if df_detail.empty:
                    break
                for _, row in df_detail.iterrows():
                    date_str = row.get("Ngay", "")
                    if not date_str:
                        continue
                    session_id = get_session_id(date_str, stock_space)
                    if session_id:
                        all_data.append({
                            "stock_id": stock_id,
                            "session_id": session_id,
                            "open_price": row.get("GiaMoCua", 0.0),
                            "close_price": row.get("GiaDongCua", 0.0),
                            "high_price": row.get("GiaCaoNhat", 0.0),
                            "low_price": row.get("GiaThapNhat", 0.0),
                            "volume": row.get("KhoiLuongKhopLenh", 0.0),
                            "matched_value": row.get("GiaTriKhopLenh", 0.0),
                            "adjust_price": row.get("GiaDieuChinh", 0.0),
                            "change_percent": row.get("ThayDoi", 0.0),
                            "updated_by": 1,
                            "created_by": 1
                        })
                page_number += 1
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error on page {page_number} for {symbol}: {e}")
                break

        # Fetch statistical data
        page_number = 1
        while True:
            data = fetch_statistical_data(symbol, page_number, start_date, end_date)
            if not data:
                break
            try:
                json_data = json.loads(data)
                if not json_data.get('Data') or not json_data['Data'].get('Data'):
                    break
                df_statistical = json_normalize(json_data['Data']['Data'])
                if df_statistical.empty:
                    break
                for _, row in df_statistical.iterrows():
                    date_str = row.get("Date", "")
                    if not date_str:
                        continue
                    session_id = get_session_id(date_str, stock_space)
                    if session_id:
                        matching_data = next((item for item in all_data if item["session_id"] == session_id and item["stock_id"] == stock_id), None)
                        if matching_data:
                            matching_data.update({
                                "buy_volume": row.get("KLDatMua", 0.0),
                                "sell_volume": row.get("KLDatBan", 0.0),
                                "net_volume": row.get("ChenhLechKL", 0.0)
                            })
                        else:
                            all_data.append({
                                "stock_id": stock_id,
                                "session_id": session_id,
                                "buy_volume": row.get("KLDatMua", 0.0),
                                "sell_volume": row.get("KLDatBan", 0.0),
                                "net_volume": row.get("ChenhLechKL", 0.0)
                            })
                page_number += 1
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error on page {page_number} for {symbol}: {e}")
                break

        if all_data:
            insert_into_db(all_data)
            print(f"Data from detail_stock_price was successfully loaded for {symbol}")