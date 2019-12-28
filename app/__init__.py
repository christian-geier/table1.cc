from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask import Flask

from whitenoise import WhiteNoise

from config import Config

csp = {
    'default-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://ajax.aspnetcdn.com',
        'https://cdn.datatables.net',
        'https://fonts.googleapis.com',
        'https://stackpath.bootstrapcdn.com',
        'https://fonts.gstatic.com'
    ]
}

app = Flask(__name__)
Talisman(app, content_security_policy=csp, force_https_permanent=True)

app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', index_file=True)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app import routes
