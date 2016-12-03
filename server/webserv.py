from flask import Flask, request, send_from_directory, redirect
from sqlalchemy import desc
from json import dumps as jsonify
from random import randint as rand
from datetime import datetime as dt
from server.database import session as db
import server.models as models

app = Flask(__name__)

def dict_to_post(data,content_type):
    p = models.Post(content=data['content'], content_type=content_type)
    if('pos_x' in data):
        p.pos_x = data['pos_x']
    else:
        p.pos_x = rand(0,99)
    if('pos_y' in data):
        p.pos_y = data['pos_y']
    else:
        p.pos_y = rand(0,99)
    if('pos_z' in data):
        p.pos_z = data['pos_z']
    else:
        p.pos_z = rand(0,99)
    if('size' in data):
        if data['size'] is 'small' or \
            data['size'] is 'medium' or \
            data['size'] is 'large':
            p.size = data['size']
        else:
            p.size = 'medium'
    else:
        p.size = rand(0,2)
    if('sender' in data):
        p.sender = data['sender']
    else:
        p.sender = "Anon"
    return p

def post_to_dict(post):
    return {
            'id':post.id,
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
def form():
    return send_from_directory('static','form.html')

@app.route("/dashboard")
def dashboard():
    return send_from_directory('static','index.html')

@app.route("/post/<int:id>/delete", methods=['POST'])
def delete_post(id):
    models.Post.query.filter_by(id=id).delete()
    db.commit()
    return redirect('dashboard')

@app.route("/post/text/", methods=['POST'])
def post_text():
    p = dict_to_post(request.form, content_type="text")
    db.add(p)
    db.commit()
    return redirect('dashboard')

@app.route("/post/photo/", methods=['POST'])
def post_photo():
    p = dict_to_post(request.form, content_type="image-url")
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
