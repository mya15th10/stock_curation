import http.client
import json
import pandas as pd
from pandas import json_normalize
from api.stock.model import db, tbt_stock
from datetime import datetime
from api.config import STOCK_REFERER_CAFEF_URL, STOCK_CAFEF_URL, STOCK_VNDIRECT_URL, STOCK_REFERER_CAFEF_URL

# Hàm lấy dữ liệu category
def fetch_categories():
    url = STOCK_CAFEF_URL
    headers = {"Accept": "application/json", "Referer": STOCK_REFERER_CAFEF_URL}

    conn = http.client.HTTPSConnection("s.cafef.vn")
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    if res.status != 200:
        print(f"status code: {res.status}")
        return None

    try:
        json_data = json.loads(data.decode("utf-8"))
        if "Data" in json_data:
            df = json_normalize(json_data["Data"])
            df.rename(columns={"Symbol": "code", "CategoryName": "category"}, inplace=True)
            return df[["code", "category"]].where(pd.notnull(df), None)
        else:
            print("No key 'Data'")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decode JSON: {e}")
        return None

# Hàm lấy stock
def fetch_data():
    headers = {
        "Accept": "application/json",
        "Referer": "STOCK_REFERER_VNDIRECT_URL",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    conn = http.client.HTTPSConnection("finfo-api.vndirect.com.vn")
    url = STOCK_VNDIRECT_URL

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    if res.status != 200:
        print(f"status code: {res.status}")
        return None

    try:
        json_data = json.loads(data.decode("utf-8"))

        if "data" in json_data:
            df = json_normalize(json_data["data"])
            df.rename(
                columns={
                    "companyName": "name",
                    "code": "code",
                    "floor": "stock_space",
                    "listedDate": "join_date",
                    "delistedDate": "leave_date",
                    "companyNameEng": "eng_name",
                    "shortName": "short_name",
                    "companyId": "id_company",
                    "taxCode": "tax_code"
                },
                inplace=True,
            )

            df = df[[
                "name",
                "eng_name",
                "short_name",
                "code",
                "stock_space",
                "join_date",
                "leave_date",
                "id_company",
                "tax_code"
            ]].where(pd.notnull(df), None)
        else:
            print("No key 'data'")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decode JSON: {e}")
        return None

    df_categories = fetch_categories()
    if df_categories is not None:
        df = pd.merge(df, df_categories, on="code", how="left")

    for i, row in df.iterrows():
        # Kiểm tra mã đã có chưa
        exist_stock = tbt_stock.query.filter_by(code = row["code"]).first()
        
        #Nếu chưa có  thì thêm
        if exist_stock is  None:
            new_stock = tbt_stock(
                name=row["name"],
                code=row["code"],
                country='VI',
                stock_space=row["stock_space"],
                join_date=row["join_date"],
                leave_date=row["leave_date"],
                init_price=0,  # Giả sử giá khởi điểm không có trong dữ liệu
                id_company=row["id_company"],
                tax_code=row["tax_code"],
                eng_name=row["eng_name"],
                short_name=row["short_name"],
                category=row["category"] if pd.notna(row["category"]) else None,
                isIndex=False
            )
            db.session.add(new_stock)
        else:
            exist_stock.name = row["name"]
            exist_stock.eng_name = row["eng_name"]
            exist_stock.short_name = row["short_name"]
            exist_stock.stock_space = row["stock_space"]
            exist_stock.join_date = row["join_date"]
            exist_stock.leave_date = row["leave_date"]
            exist_stock.id_company = row["id_company"]
            exist_stock.tax_code = row["tax_code"]
            exist_stock.category = row["category"] if pd.notna(row["category"]) else None

    db.session.commit()


