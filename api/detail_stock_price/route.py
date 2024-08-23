from flask import Blueprint, jsonify, request
from api.detail_stock_price.service import fetch_detail_stock_data

detail_stock_price = Blueprint('detail_stock_price_operations', __name__, url_prefix='/detail_stock_price')

@detail_stock_price.route('/update', methods=['POST'])
def update_detail_stock_price():
    fetch_detail_stock_data()
    return jsonify({"message": "Detail stock price data updated successfully"}), 200