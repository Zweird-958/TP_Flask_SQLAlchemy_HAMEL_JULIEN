from flask import jsonify

def send_error(message):
    return jsonify({
        "success": False,
        "message": message
    })

def send_success(message):
    return jsonify({
        "success": True,
        "message": message
    })