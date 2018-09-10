from flask import render_template

from app import app


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'Ok'


@app.route('/login')
def index():
    return render_template('login.html', title='Login')
