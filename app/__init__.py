from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask import Flask

from whitenoise import WhiteNoise

from config import Config

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', index_file=True)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
Talisman(app, force_https_permanent=True)

from app import routes
