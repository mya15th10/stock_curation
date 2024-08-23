from flask import Blueprint, jsonify, request
from api.session.service import up_session_db

session = Blueprint('session_operations', __name__, url_prefix='/session')

@session.route('/update', methods=['POST'])
def update_sessions():
    if request.is_json:
        data = request.get_json()
        symbols = data.get("symbols", [])
        for symbol in symbols:
            up_session_db(symbol)
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"error": "Unsupported Media Type. Content-Type should be application/json."}), 415