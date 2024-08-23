from flask import Blueprint, jsonify, request
from api.stock.service import fetch_data

stock = Blueprint('tbt_stock_operations', __name__, url_prefix='/stock')

@stock.route('/update', methods=['POST'])
def update_stocks():
    fetch_data()
    return jsonify({"message": "Stock data updated successfully"}), 200