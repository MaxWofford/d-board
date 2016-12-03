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

@app.route("/post/text/", methods=['POST'])
def post_text():
    p = models.Post(content=request.form['content'], content_type="text")
    if('pos_x' in request.form):
        p.pos_x = request.form['pos_x']
    if('pos_y' in request.form):
        p.pos_y = request.form['pos_y']
    if('pos_z' in request.form):
        p.pos_z = request.form['pos_z']
    if('size' in request.form):
        p.size = request.form['size']
    if('sender' in request.form):
        p.sender = request.form['sender']
    db.add(p)
    db.commit()
    return redirect('dashboard')

@app.route("/post/photo/", methods=['POST'])
def post_photo():
    p = models.Post(content=request.form['content'], content_type="image-url")
    if('pos_x' in request.form):
        p.pos_x = request.form['pos_x']
    if('pos_y' in request.form):
        p.pos_y = request.form['pos_y']
    if('pos_z' in request.form):
        p.pos_z = request.form['pos_z']
    if('size' in request.form):
        p.size = request.form['size']
    if('sender' in request.form):
        p.sender = request.form['sender']
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
