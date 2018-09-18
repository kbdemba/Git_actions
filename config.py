import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join('/db', 'sso_example.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
