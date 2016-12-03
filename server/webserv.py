from flask import Flask, request, send_from_directory, redirect
from sqlalchemy import desc
from json import dumps as jsonify
from random import randint as rand
from datetime import datetime as dt
from server.database import session as db
import server.models as models

app = Flask(__name__)

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
    p = models.Post(content=request.form['content'], content_type="text")
    if('pos_x' in request.form):
        p.pos_x = request.form['pos_x']
    else:
        p.pos_x = rand(0,99)
    if('pos_y' in request.form):
        p.pos_y = request.form['pos_y']
    else:
        p.pos_y = rand(0,99)
    if('pos_z' in request.form):
        p.pos_z = request.form['pos_z']
    else:
        p.pos_z = rand(0,99)
    if('size' in request.form):
        if request.form['size'] is 'small' or \
            request.form['size'] is 'medium' or \
            request.form['size'] is 'large':
            p.size = request.form['size']
        else:
            p.size = 'medium'
    else:
        p.size = rand(0,2)
    if('sender' in request.form):
        p.sender = request.form['sender']
    else:
        p.sender = "Anon"
    db.add(p)
    db.commit()
    return redirect('dashboard')

@app.route("/post/photo/", methods=['POST'])
def post_photo():
    p = models.Post(content=request.form['content'], content_type="image-url")
    if('pos_x' in request.form):
        p.pos_x = request.form['pos_x']
    else:
        p.pos_x = rand(0,99)
    if('pos_y' in request.form):
        p.pos_y = request.form['pos_y']
    else:
        p.pos_y = rand(0,99)
    if('pos_z' in request.form):
        p.pos_z = request.form['pos_z']
    else:
        p.pos_z = rand(0,99)
    if('size' in request.form):
        p.size = request.form['size']
    else:
        p.size = rand(0,2)
    if('sender' in request.form):
        p.sender = request.form['sender']
    else:
        p.sender = "Anon"
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
