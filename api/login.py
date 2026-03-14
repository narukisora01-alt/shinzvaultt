from flask import Flask, redirect
import os

app = Flask(__name__)

CLIENT_ID    = os.environ.get("DISCORD_CLIENT_ID")
REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")

@app.route("/api/login")
@app.route("/")
def login():
    return redirect(
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )
