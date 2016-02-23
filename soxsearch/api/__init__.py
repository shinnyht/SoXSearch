import json
import time

from flask import (
    jsonify,
    render_template,
    request
)
from flask.ext.cors import CORS, cross_origin
from searcher import Searcher
from soxsearch import app

searcher = Searcher(
    "hostname", # set hostname
    "db",       # set database
    "username", # set MySQL username
    "passwd",   # set password
    "utf8"
)

@app.route("/api/search", methods=["GET"])
@cross_origin()
def search_nodes():
    name = None
    datatype = None
    latitude = None
    longitude = None
    radius = 10

    start = time.time()

    if request.args.has_key("name"):
        name = request.args["name"]
    if request.args.has_key("type"):
        datatype = request.args["type"]
    if request.args.has_key("radius"):
        radius = float(request.args["radius"])
    if set(("lat", "lng")) <= set(location):
        latitude = request.args["lat"]
        longitude = request.args["lng"]


    result = searcher.searchNodes(
        name,
        datatype,
        latitude,
        longitude,
        radius
    )

    goal = time.time() - start
    result["time"] = str(goal) + " sec"

    json_result = json.dumps(
        result,
        ensure_ascii=False
    ).encode("utf8")

    return json_result

