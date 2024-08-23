from flask import Blueprint, jsonify, request
from api.stock.service import fetch_data as fetch_stock_data
from api.session.service import up_session_db as update_session_data
from api.detail_stock_price.service import fetch_detail_stock_data as update_detail_stock_data

update_all_data = Blueprint('all_data', __name__, url_prefix = '/all_data')

@update_all_data.route('/update', methods=['POST'])
def update_data():
    try:
        # Update stock data
        fetch_stock_data()
        print("Stock data updated successfully.")

        # Update session data for each index
        for index in ["HNX-INDEX", "UPCOM-INDEX", "VNINDEX"]:
            update_session_data(index)
        print("Session data updated successfully.")

        # Update detail stock price data
        update_detail_stock_data()
        print("Detail stock price data updated successfully.")


        #jsonify của Flask dùng để tạo ra một response JSON
        return jsonify({"message": "All data updated successfully"}), 200
    except Exception as e:
        print(f"Error updating data: {e}")
        return jsonify({"message": "Error updating data", "error": str(e)}), 500

