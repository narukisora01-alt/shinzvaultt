from flask import Flask, request, jsonify
import os, jwt

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY", "shinzvault_secret")

@app.route("/api/me")
@app.route("/")
def me():
    token = request.cookies.get("sv_token")
    if not token:
        return jsonify({"error": "not logged in"}), 401
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify(payload)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "invalid token"}), 401
