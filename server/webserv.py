from flask import Flask, request, send_from_directory
from json import dumps as jsonify
from datetime import datetime as dt
from server.database import session as db
import server.models as models

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"

@app.route("/dashboard")
def dashboard():
    return send_from_directory('static','index.html')

@app.route("/dashboard.json")
def dashboard_json():
    return send_from_directory('static','example.json')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()
