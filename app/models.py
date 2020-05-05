from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=False)
    firstname = db.Column(db.String(64), index=False)
    lastname = db.Column(db.String(64), index=False)
    images = db.relationship('SigninImage', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class SigninImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))