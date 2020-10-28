import sys

from requests.models import Request
sys.dont_write_bytecode = True

import json
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

from constants import *
from sources.source import source

@app.route('/api/')
@cross_origin()
def getsources():
    return json.dumps(misc.Sources)

@app.route('/api/<src>')
@app.route('/api/<src>/<int:n>')
@cross_origin()
def next(src, n:int = 0):
    q = request.args.get("q") if "q" in request.args.keys() else request.query_string.decode()
    return json.dumps(source(src).GetNext(n,q))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')