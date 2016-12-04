import requests
from flask import Flask, request, send_from_directory, redirect
from sqlalchemy import desc
from json import dumps as jsonify
from random import randint as rand
from datetime import datetime as dt
from server.database import session as db
import server.models as models
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
import os

app = Flask(__name__)
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME','d-board.app.csh.rit.edu')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','d-board-illuminati')

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()

OIDC_ISSUER = os.environ.get('OIDC_ISSUER', 'https://sso.csh.rit.edu/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': os.environ.get('OIDC_CLIENT_ID', 'd-board'),
    'client_secret': os.environ.get('OIDC_CLIENT_SECRET', ''),
    'post_logout_redirect_uris': [os.environ.get('OIDC_LOGOUT_REDIRECT_URI', 'http://d-board.app.csh.rit.edu/logout')]
}

auth = OIDCAuthentication(app,
                          issuer=OIDC_ISSUER,
                          client_registration_info=OIDC_CLIENT_CONFIG)



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
        p.size = data['size']
    else:
        p.size = 'medium'
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
@auth.oidc_auth
def form():
    return send_from_directory('static','form.html')

@app.route("/dashboard")
def dashboard():
    return send_from_directory('static','dashboard.html')

@app.route("/post/<int:id>/delete", methods=['POST'])
@auth.oidc_auth
def delete_post(id):
    models.Post.query.filter_by(id=id).delete()
    db.commit()
    return redirect('dashboard')

@app.route("/post/text", methods=['POST'])
@auth.oidc_auth
def post_text():
    p = dict_to_post(request.get_json(), content_type="text")
    db.add(p)
    db.commit()
    return jsonify(post_to_dict(p))

@app.route("/post/photo", methods=['POST'])
@auth.oidc_auth
def post_photo():
    p = dict_to_post(request.get_json(), content_type="image-url")
    db.add(p)
    db.commit()
    return jsonify(post_to_dict(p))

@app.route("/post/youtube", methods=['POST'])
@app.oidc_auth
def post_youtube():
    p = dict_to_post(request.get_json(), content_type="youtube-id")
    db.add(p)
    db.commit()
    return jsonify(post_to_dict(p))

@app.route("/dashboard.json")
def dashboard_json():
    posts = models.Post.query.order_by(desc(models.Post.timestamp)).limit(10).all()
    resp = []
    for post in reversed(posts):
        resp.append(post_to_dict(post))
    return jsonify({"boards":resp})

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

@app.route('/logout')
@auth.oidc_logout
def logout():
    return redirect(url_for('index'), 302)
