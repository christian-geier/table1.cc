from flask_bootstrap import Bootstrap

from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app import routes
