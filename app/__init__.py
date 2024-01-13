from urllib.parse import quote
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightmanagement?charset=utf8mb4" % quote('!Tinhyeu123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "BG\xeb\xdd\t\xf1\x93\xbeWp\xbb\xffla V"

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
principals = Principal(app)