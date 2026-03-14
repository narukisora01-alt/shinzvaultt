from flask import Flask, redirect, request, make_response, jsonify
import requests, os, jwt, time

app = Flask(__name__)

CLIENT_ID     = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
REDIRECT_URI  = os.environ.get("DISCORD_REDIRECT_URI")
SECRET_KEY    = os.environ.get("SECRET_KEY", "shinzvault_secret")

@app.route("/api/login")
def login():
    return redirect(
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )

@app.route("/api/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect("/login.html")

    token_res = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    access_token = token_res.json().get("access_token")
    if not access_token:
        return redirect("/login.html")

    user_res = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user = user_res.json()

    payload = {
        "id":          str(user.get("id", "")),
        "username":    user.get("username", ""),
        "global_name": user.get("global_name") or user.get("username", ""),
        "avatar":      user.get("avatar", ""),
        "exp":         int(time.time()) + 60 * 60 * 24 * 7
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    response = make_response(redirect("/dashboard.html"))
    response.set_cookie(
        "sv_token", token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )
    return response

@app.route("/api/me")
def me():
    token = request.cookies.get("sv_token")
    if not token:
        return jsonify({"error": "not logged in"}), 401
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify(payload)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "invalid token"}), 401

@app.route("/api/logout")
def logout():
    response = make_response(redirect("/login.html"))
    response.delete_cookie("sv_token", path="/")
    return response
