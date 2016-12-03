from flask import Flask, request, send_from_directory, redirect
from sqlalchemy import desc
from json import dumps as jsonify
from datetime import datetime as dt
from server.database import session as db
import server.models as models

app = Flask(__name__)

def post_to_dict(post):
    return {
            'type':post.content_type,
            'sender':post.sender,
            'timestamp':post.timestamp.timestamp(),
            'content':post.content,
            'size':post.size,
            'location': {
                'x':post.pos_x,
                'y':post.pos_y,
                'z':post.pos_z
            }
        }

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"

@app.route("/dashboard")
def dashboard():
    return send_from_directory('static','index.html')

@app.route("/post/text/<text>")
def post_text(text):
    p = models.Post(content=text, content_type="text")
    db.add(p)
    db.commit()
    return redirect('dashboard')

@app.route("/dashboard.json")
def dashboard_json():
    posts = models.Post.query.order_by(desc(models.Post.timestamp)).limit(10).all()
    resp = []
    for post in posts:
        resp.append(post_to_dict(post))
    return jsonify({"boards":resp})

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()
