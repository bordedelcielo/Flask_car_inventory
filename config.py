import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
        Set Config variables for the flask app
        using Environment variables where available.
        Create config variables if not done already.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False