import json

from flask import (
    jsonify,
    render_template,
    request
)
from searcher import Searcher
from soxsearch import app

searcher = Searcher(
    "hostname",
    "db",
    "username",
    "passwd",
    "utf8"
)

@app.route('/api/search/name', methods=['GET'])
def search_by_name():
    name = request.args["name"]
    result = searcher.searchByName(name)

    json_result = json.dumps(
        result,
        ensure_ascii=False
    ).encode('utf8')

    return json_result


@app.route('/api/search/location', methods=['GET'])
def search_by_location():
    latitude = float(request.args["lat"])
    longitude = float(request.args["lng"])
    radius = float(request.args["radius"])

    result = searcher.searchByLocation(
        latitude,
        longitude,
        radius
    )

    json_result = json.dumps(
        result,
        ensure_ascii=False
    ).encode('utf8')

    return json_result


@app.route('/api/search/type', methods=['GET'])
def search_by_type():
    datatype = request.args["type"]
    result = searcher.searchByType(datatype)

    json_result = json.dumps(
        result,
        ensure_ascii=False
    ).encode('utf8')

    return json_result

