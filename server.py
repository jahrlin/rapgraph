from flask import Flask
from flask import render_template
from firebase import firebase
import requests
import graphene
from classes.song import *


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('master.html', title='Rapgraph - Index', song = None)


@app.route('/graph/')
@app.route('/graph/<id>')
def graph(id=None):
    fb = firebase.FirebaseApplication('firebase url', None)
    headers = {'Authorization': 'Bearer ' + 'insert genius api token here'}
    r = requests.get('https://api.genius.com/songs/265', headers=headers)
    
    data = obj(r.json())
    song = Song(artist = data.response.song.primary_artist.name);

    return render_template('master.html', title='Graph #'+id, song = song)

if __name__ == '__main__':
    app.debug = True
    app.run()

