from api.extension import db
from datetime import datetime

class tbt_session(db.Model):
    __tablename__ = 'tbt_session'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quarter = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Float, nullable=False, default=0)
    stock_space = db.Column(db.Integer, nullable = True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, quarter, day_of_week, day_of_month, month, year, volume, stock_space, updated_at, created_at, updated_by, created_by):
        self.quarter = quarter
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.month = month
        self.year = year
        self.volume = volume
        self.stock_space = stock_space
        self.updated_at = updated_at
        self.created_at = created_at
        self.updated_by = updated_by
        self.created_by = created_by