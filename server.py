from classes.song import *
from flask import Flask, render_template
from firebase import firebase
import requests
import logging
from flask import request
import json
from data import setup
from schema import schema
from pprint import pprint


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

'''readonly url, create your own if you want to write'''
dbUrl = 'https://rapgraphdb.firebaseio.com/'

'''genius api token'''
token = ''

data = setup(db=dbUrl, token=token)


@app.route('/')
def index():
    global data

    query = '''
        query songQuery {
            songs {
                edges {
                    node {
                        id
                        title
                        url
                        primaryartist {
                            edges {
                                node {
                                    id
                                    name
                                }
                            }
                        }
                        sampledsongs {
                            edges {
                                node {
                                    id
                                    title
                                }
                            }
                        }
                        samplingsongs {
                            edges {
                                node {
                                    id
                                    title
                                }
                            }
                        }
                    }
                }
            }
        }
    '''
    result = schema.execute(query)
    errors = result.errors

    pprint(errors)

    edges = list(result.data.values())[0]['edges']

    return render_template(
            'start.html',
            title='Rapgraph - Index',
            data=edges,
            result=json.dumps(result.data).replace("'", "&#39;"))


@app.route('/songs/add/<song_id>', methods=['GET', 'POST'])
def addSong(song_id):

    if request.method == 'GET':
        id = song_id
        if id is not None:
            fb = firebase.FirebaseApplication(
                    'https://rapgraphdb.firebaseio.com/',
                    None)

            headers = {
                    'Authorization':
                    'Bearer ' + token
                    }

            r = requests.get(
                    'https://api.genius.com/songs/' + id,
                    headers=headers)

            fb.post('/songs', r.json()['response']['song'])

            return render_template(
                    'start.html',
                    text='Added song ' + song_id)
        else:
            return render_template('songs/add.html', title='Missing song ID')
    else:
        return render_template('songs/add.html', title='Add song')


if __name__ == '__main__':
    app.debug = True
    app.run()
