from flask import (
    render_template
)
from soxsearch import app

@app.route('/', methods=['GET'])
def soxsearch_home():
    return render_template("soxsearch.jinja2.html")


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.jinja2.html'), 404


# 429 page
@app.errorhandler(429)
def too_many_requests(e):
    return render_template('error/429.jinja2.html'), 429


# 500 page
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.jinja2.html'), 500


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("img/sox_logo.png")
