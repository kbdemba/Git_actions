import os

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
import requests

from app import app, db
from app.models import User, SigninImage


class InvalidUsage(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'Ok'


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
@app.route('/welcome', methods=['GET'])
@login_required
def welcome():
    return render_template('welcome.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    if request.method == 'POST':
        data = request.form
        facerec_response = requests.post(
            f'http://{os.environ.get("FACEREC_ADDRESS")}/get_emb',
            data=data['img']
        )
        embs = facerec_response.json().get('embs')
        if len(embs) != 1:
            return render_template('login.html', title='Login')
        emb = embs[0]
        nn_search_response = requests.post(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/find',
            json={'vector': emb}
        )
        nn_search = nn_search_response.json()
        print(nn_search)
        if nn_search.get('distance', 1000) > .6:
            return render_template('login.html', title='Login')
        photo = SigninImage.query.filter_by(search_index=nn_search.get('index')).first()
        login_user(photo.user)
        return redirect(url_for('welcome'))
    return render_template('login.html', title='Login')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    if request.method == 'POST':
        data = request.form
        facerec_response = requests.post(
            f'http://{os.environ.get("FACEREC_ADDRESS")}/get_emb',
            data=data['img']
        )
        embs = facerec_response.json().get('embs')
        if len(embs) != 1:
            raise InvalidUsage('Photo must have exactly 1 face')
        emb = embs[0]
        nn_search_response = requests.post(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/add',
            json={'vector': emb}
        )
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']

        user = User(firstname=firstname, lastname=lastname, email=email)
        nn_index = SigninImage(
            search_index=nn_search_response.json().get('index'),
            user=user
        )
        db.session.add(user)
        db.session.add(nn_index)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up')
