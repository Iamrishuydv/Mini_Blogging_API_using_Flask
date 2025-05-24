from http import HTTPStatus as status
from flask import jsonify

# Custom response function for same structure of response through oout the application
def custom_response(status_str, data=None, message=None, status_code=status.OK):
    response_data = {
        "status": 1 if status_str == "success" else 0,
        "success": True if status_str == "success" else False
    }
    if data is not None:
        response_data["data"] = data
    if message is not None:
        response_data["message"] = message
    return jsonify(response_data), status_code