from flask import *
from .webs.webs import websBP
from .programadores.programadores import programadoresBP

app = Flask(__name__)

app.register_blueprint(programadoresBP, url_prefix='/programadores')
app.register_blueprint(websBP, url_prefix='/webs')