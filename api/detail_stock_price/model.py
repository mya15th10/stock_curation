from api.extension import db
from datetime import datetime

class tbt_detail_stock_price(db.Model):
    __tablename__ = 'tbt_detail_stock_price'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('tbt_stock.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('tbt_session.id'), nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    ceiling_price = db.Column(db.Float, nullable=False, default=0.0) 
    floor_price = db.Column(db.Float, nullable=False, default=0.0) 
    volume = db.Column(db.Float, nullable=False)
    buy_volume = db.Column(db.Float, nullable=False, default=0.0)
    sell_volume = db.Column(db.Float, nullable=False, default=0.0)
    net_volume = db.Column(db.Float, nullable=False, default=0.0)
    matched_value = db.Column(db.Float, nullable=False, default=0.0)
    adjust_price = db.Column(db.Float, nullable=False, default=0.0)
    change_percent = db.Column(db.Float, nullable=False, default=0.0)
    outstanding_share = db.Column(db.Float, nullable=False, default=0.0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, nullable=False, default=1)

    stock = db.relationship('tbt_stock', backref=db.backref('detail_prices', lazy=True))
    session = db.relationship('tbt_session', backref=db.backref('detail_prices', lazy=True))

    def __init__(self, stock_id, session_id, open_price, close_price, high_price, low_price, ceiling_price, floor_price, volume, buy_volume, sell_volume, net_volume, matched_value, adjust_price, change_percent, outstanding_share, updated_by=1, created_by=1):
        self.stock_id = stock_id
        self.session_id = session_id
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.ceiling_price = ceiling_price
        self.floor_price = floor_price
        self.volume = volume
        self.buy_volume = buy_volume
        self.sell_volume = sell_volume
        self.net_volume = net_volume
        self.matched_value = matched_value
        self.adjust_price = adjust_price
        self.change_percent = change_percent
        self.outstanding_share = outstanding_share
        self.updated_by = updated_by
        self.created_by = created_by
