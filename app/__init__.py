from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES
from threading import Thread, Lock
from app.models.base import BaseModel


assets = Environment()
db = SQLAlchemy(model_class=BaseModel)
loginManager = LoginManager()
mail = Mail()
