import os

from flask import Flask
from flaskext.mysql import MySQL

UPLOAD_FOLDER = 'static'

# __name__ = a built in var. in py. contains - '__main__' ??? PASS.
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'lifgames_railroad'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'nnd;fwjdwmfhgsktkrlv#kfWuf'  # ĉuk laboro estas fike.
mysql.init_app(app)

__all__ = [
    'OK',
    'ERR_SAME_NICK',
    'ERR_SAME_ID',
    'ERR_EMAIL_EXIST',
    'ERR_PWD_INCORRECT'
]

# template_dir = os.path.abspath('/src/templates')

from .src import views, player_view