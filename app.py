from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "APP HIDUP"

@app.route("/ping")
def ping():
    return "OK"