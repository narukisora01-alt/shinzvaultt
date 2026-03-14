from flask import Flask, redirect, make_response

app = Flask(__name__)

@app.route("/api/logout")
@app.route("/")
def logout():
    resp = make_response(redirect("/login.html"))
    resp.delete_cookie("sv_token", path="/")
    return resp
