from flask import Flask, request
from json import dumps as jsonify
from datetime import datetime as dt
from server.database import session as db
import server.models as models

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()
