from flask import Flask
from flaskext.mysql import MySQL

# __name__ = a built in var. in py. contains - '__main__' ??? PASS.
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'lifgames_railroad'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)