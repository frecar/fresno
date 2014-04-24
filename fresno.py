# -*- coding: utf-8 -*-

import json
import requests

from flask import Flask, make_response

app = Flask(__name__)
app.debug = True


@app.route('/<title>/actors')
def actors(title):
    csv = "Name\n"

    url = "https://www.googleapis.com/freebase/v1/mqlread?query=[{%20%22name%22:%20%22"
    url += title
    url += "%22,%20%22mid%22:%20null,%20%22starring%22:%20[{%20%22actor%22:%20[{%20%22" \
           "name%22:%20null%20}]%20}],%20%22country%22:%20[{%20%22name%22:%20%22" \
           "Norway%22%20}],%20%22type%22:%20%22/film/film%22%20}]"

    r = requests.get(url)
    text = r.text.decode('unicode-escape')
    starring = json.loads(text)['result'][0]['starring']

    for actor in starring:
        csv += "%s \n" % actor['actor'][0]['name']

    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser

    response.headers["Content-Disposition"] = "attachment; filename=actors.csv"
    return response


@app.route('/actor/<actor>/norwegian-movies')
def movies_by_actor(actor):
    csv = "Name\n"

    url = "https://www.googleapis.com/freebase/v1/mqlread?query=[{%20%22name%22:%20null," \
          "%20%22mid%22:%20null,%20%22starring%22:%20[{%20%22actor%22:%20[{%20%22name%22:%20%22"
    url += actor
    url += "%22%20}]%20}],%20%22country%22:%20[{%20%22name%22:%20%22Norway%22%20}]," \
           "%20%22type%22:%20%22/film/film%22%20}]"

    r = requests.get(url)
    text = r.text.decode('unicode-escape')
    result = json.loads(text)['result']

    for movie in result:
        csv += "%s \n" % movie['name']

    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser

    response.headers["Content-Disposition"] = "attachment; filename=movies.csv"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')