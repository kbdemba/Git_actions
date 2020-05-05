import os

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
import requests

from app import app, db
from app.models import User, SigninImage


NN_KEY_DIFFERENCE = 10
NN_SEARCH_KEY = 1


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
    wrong
    return 'Ok ok'   


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


@app.route('/delete')
def delete_account():
    images = current_user.images
    for image in images:
        key = image.id + NN_KEY_DIFFERENCE
        nn_search_response = requests.delete(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/databases/db/features/{key}'
        )
        if nn_search_response.status_code != 200:
            raise('Feature vector deletion failed')
        db.session.delete(image)
    db.session.delete(current_user)
    logout_user()
    db.session.commit()
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

        nn_search_response = requests.put(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/databases/db/features/{NN_SEARCH_KEY}',
            json={'features': emb}
        )

        nn_search_response = requests.get(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/search?database=db&key={NN_SEARCH_KEY}&limit=2'
        )
        nn_search = nn_search_response.json()
        distances = nn_search.get('distances', [])
        indexes = nn_search.get('indexes', [])
        if len(distances) < 2 or distances[1] > .6:
            return render_template('login.html', title='Login')
        photo = SigninImage.query.get(indexes[1] - NN_KEY_DIFFERENCE)
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

        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']

        user = User(firstname=firstname, lastname=lastname, email=email)
        nn_index = SigninImage(user=user)
        db.session.add(user)
        db.session.add(nn_index)
        db.session.flush()

        key = nn_index.id + NN_KEY_DIFFERENCE
        nn_search_response = requests.put(
            f'http://{os.environ.get("NN_SEARCH_ADDRESS")}/databases/db/features/{key}',
            json={'features': emb}
        )

        if nn_search_response.status_code != 200:
            raise ('Problem storing embedding')

        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up')
