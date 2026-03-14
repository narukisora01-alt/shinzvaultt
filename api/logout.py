from flask import Flask, redirect, make_response

app = Flask(__name__)

@app.route("/api/logout")
@app.route("/")
def logout():
    response = make_response(redirect("/login.html"))
    response.delete_cookie("sv_token", path="/")
    return response
