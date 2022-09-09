from flask import jsonify

from main import app


@app.get("/ping")
def ping():
    return jsonify({'message': 'pong'})
