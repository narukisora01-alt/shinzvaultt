from flask import Flask, redirect, request, session
import requests, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

CLIENT_ID     = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
REDIRECT_URI  = os.environ.get("DISCORD_REDIRECT_URI")

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
    res = requests.post("https://discord.com/api/oauth2/token", data={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  REDIRECT_URI,
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = res.json().get("access_token")
    user  = requests.get("https://discord.com/api/users/@me", headers={
        "Authorization": f"Bearer {token}"
    }).json()

    session["user"] = user
    return redirect("/dashboard.html")

@app.route("/api/me")
def me():
    return session.get("user", {"error": "not logged in"})
