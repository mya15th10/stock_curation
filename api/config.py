import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Đảm bảo rằng biến môi trường DATABASE_URL được thiết lập chính xác
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Tắt theo dõi các sửa đổi của SQLAlchemy để tránh cảnh báo
SECRET_KEY = os.environ.get('KEY')
DEBUG = True  # Để True để hiện thông báo lỗi chi tiết


#URL File service của module stock
STOCK_CAFEF_URL = "https://s.cafef.vn/ajax/pagenew/databusiness/congtyniemyet.ashx?centerid=0&skip=0&take=9999&major=0"
STOCK_VNDIRECT_URL = "/v4/stocks?q=type:stock,ifc~floor:HOSE,HNX,UPCOM&size=9999"
STOCK_REFERER_CAFEF_URL = "https://s.cafef.vn/"
STOCK_REFERER_VNDIRECT_URL = "https://dstock.vndirect.com.vn/du-lieu-thi-truong/lich-su-gia"


#URL file service của module session
SESSION_CAFEF_URL = "/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={symbol}&StartDate={start_date}&EndDate={end_date}&PageIndex={page_number}&PageSize=20"
SESSION_REFERER_URL = "https://s.cafef.vn/"

#URL file service của module detail_stock_price
DETAIL_CAFEF_URL = "/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={symbol}&StartDate={start_date}&EndDate={end_date}&PageIndex={page_number}&PageSize=20"
DETAIL_CAFEF_STATISTICAL_URL = "/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={symbol}&StartDate={start_date}&EndDate={end_date}&PageIndex={page_number}&PageSize=20"
DETAIL_CAFEF_REFERER_URL = "https://s.cafef.vn/du-lieu-doanh-nghiep.chn"