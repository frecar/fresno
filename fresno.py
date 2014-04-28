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


@app.route('/movie/<title>/genre')
def genre(title):
    csv = "Genre\n"

    url = "https://www.googleapis.com/freebase/v1/mqlread?query=[{%20%22name%22:%20%22"
    url += title
    url += "%22,%20%22mid%22:%20null,%20%22genre%22:%20[{%20%22name%22:%20null%20}]," \
           "%20%22type%22:%20%22/film/film%22%20}]"

    r = requests.get(url)
    text = r.text.decode('unicode-escape')
    result = json.loads(text)['result']

    csv += '"'
    for movie in result[0]['genre']:
        genre = movie['name'].lower().capitalize()
        csv += '%s, ' % genre
    csv += '"'

    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser

    response.headers["Content-Disposition"] = "attachment; filename=genre.csv"
    return response


@app.route('/movie/<title>/meta')
def meta(title):
    csv = "Name, runtime, initial_release_date, directed_by, topic\n"

    url = "https://www.googleapis.com/freebase/v1/mqlread?query=[{%20%22name%22:%20%22"
    url += title
    url += "%22,%20%22mid%22:%20null,%20%22runtime%22:%20[{%20%22runtime%22:%20null," \
           "%20%22limit%22:%201%20}],%20%22country%22:%20[{%20%22name%22:%20null%20}]," \
           "%20%22primary_language%22:%20null,%20%22initial_release_date%22:%20null,%20%" \
           "22directed_by%22:%20[{%20%22name%22:%20null%20}]," \
           "%20%22type%22:%20%22/film/film%22%20}]"

    r = requests.get(url)
    text = r.text.decode('unicode-escape')
    meta_data = json.loads(text)['result'][0]

    mid = meta_data['mid']

    topic_data = ""

    try:
        topic_url = "https://www.googleapis.com/freebase/v1/topic%s?filter=/common/topic" % mid

        r = requests.get(topic_url)
        text = r.text
        topic_data_values = json.loads(text)["property"]['/common/topic/article']["values"]

        for topic in topic_data_values:
            for topic_text in topic['property']['/common/document/text']['values']:
                topic_data += topic_text['value']

    except:
        pass

    try:
        runtime = meta_data['runtime'][0]['runtime']
    except:
        runtime = ""

    directors = '"'
    for director in meta_data['directed_by']:
        directors += director['name'] + ","

    directors = directors[0:len(directors)-1] + '"'

    csv += "%s, %s, %s, %s, %s" % (meta_data['name'], runtime,
                                   meta_data['initial_release_date'],
                                   directors, topic_data)

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