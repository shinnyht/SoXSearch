from flask import Flask

def createApp():
    """ Flask application factory"""

    # setup Flask app and app.config
    app = Flask(__name__)
    return app


app = createApp()

import apps
import api
