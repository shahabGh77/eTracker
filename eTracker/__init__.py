from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_session_captcha import FlaskSessionCaptcha

login_manager = LoginManager()
db = MongoEngine()
app = Flask(__name__)

app.config.from_object(Config)
login_manager.init_app(app)
db.init_app(app)
captcha = FlaskSessionCaptcha(app)

from eTracker import routes