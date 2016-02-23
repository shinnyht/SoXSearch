from flask import Flask
from flask.ext.cors import CORS

def createApp():
    """ Flask application factory"""

    # setup Flask app and app.config
    app = Flask(__name__)
    return app


app = createApp()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

import apps
import api
