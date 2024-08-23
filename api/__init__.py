from flask import Flask
from api.stock.route import stock
from api.session.route import session
from api.detail_stock_price.route import detail_stock_price
from api.route import update_all_data
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from api.extension import db, ma

def create_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
    db.create_all(app=app)
    print("created DB")

def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    ma.init_app(app)
    
    # Đăng ký Blueprint
    app.register_blueprint(stock, url_prefix='/stock')
    app.register_blueprint(session, url_prefix='/session')
    app.register_blueprint(detail_stock_price, url_prefix='/detail_stock_price')
    app.register_blueprint(update_all_data, url_prefix='/all_data')

    return app
