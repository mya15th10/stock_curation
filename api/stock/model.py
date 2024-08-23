from api.extension import db
from datetime import datetime

class tbt_stock(db.Model):
    __tablename__ = 'tbt_stock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1024), nullable=True)
    id_company = db.Column(db.Integer, nullable=True)
    tax_code = db.Column(db.Integer, nullable=True)
    eng_name = db.Column(db.String(1024), nullable=True)
    short_name = db.Column(db.String(200), nullable=True)
    eng_short_name = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    country = db.Column(db.String(4), nullable=False, default='VI')
    stock_space = db.Column(db.String(16), nullable=False)
    join_date = db.Column(db.DateTime, nullable=True)
    leave_date = db.Column(db.DateTime, nullable=True)
    init_price = db.Column(db.Float, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, nullable=False, default=1)
    category = db.Column(db.String(255), nullable=True)

    def __init__(self, code, country, stock_space, join_date, leave_date, init_price, name, id_company=None, tax_code=None, eng_name='', short_name='', eng_short_name='', category=None, isIndex=False):
        self.code = code
        self.country = country
        self.stock_space = stock_space
        self.join_date = join_date
        self.leave_date = leave_date
        self.init_price = init_price
        self.name = name
        self.id_company = id_company
        self.tax_code = tax_code
        self.eng_name = eng_name
        self.short_name = short_name
        self.eng_short_name = eng_short_name
        self.category = category
        self.isIndex = isIndex
      
