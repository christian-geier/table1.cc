from flask_bootstrap import Bootstrap

from flask import Flask

from whitenoise import WhiteNoise

from config import Config

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', index_file=True)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app import routes
