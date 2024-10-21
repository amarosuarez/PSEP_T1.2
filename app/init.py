from flask import *

from app.webs.webs import websBP
from app.programadores.programadores import programadoresBP
from app.users.routes import usersBP
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'miclave'
jwt = JWTManager(app)

app.register_blueprint(usersBP, url_prefix='/users')
app.register_blueprint(programadoresBP, url_prefix='/programadores')
app.register_blueprint(websBP, url_prefix='/webs')