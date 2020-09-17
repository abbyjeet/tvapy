import sys
sys.dont_write_bytecode = True

import json
from flask import Flask

app = Flask(__name__)

from constants import *
from sources.source import source

# @app.route('/test')
# def test():
#     import requests
#     from bs4 import BeautifulSoup

#     source = requests.get("https://coreyms.com").text
#     soup = BeautifulSoup(source, 'lxml')
#     headers = soup.select("article header")
#     out = []
#     for h in headers:
#         out.append({
#             "title":h.h2.text,
#             "datetime":h.time.text
#         })

#     return json.dumps(out)

@app.route('/')
def sources():
    return json.dumps(misc.Sources)

@app.route('/<src>')
@app.route('/<src>/<encurl>')
def channels(src, encurl=""):
    return json.dumps(source(src).GetChannels(encurl))

@app.route('/<src>/s/<encurl>')
def shows(src, encurl):
    return json.dumps(source(src).GetShows(encurl))
    
@app.route('/<src>/e/<encurl>')
def episodes(src, encurl):
    return json.dumps(source(src).GetEpisodes(encurl))

@app.route('/<src>/p/<encurl>')
def playdata(src, encurl):
    return json.dumps(source(src).GetPlayData(encurl))