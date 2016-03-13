from flask import Flask
from flask import render_template
import requests

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

    headers = {'Authorization': 'Bearer ' + 'qTQDqeQ5NWgbqCBN8-5uVnm-9HmmkkD6_XErXOgPNn7q3CFQPdoGHCNe6hm4lpry'}
    r = requests.get('https://api.genius.com/songs/265', headers=headers)
    
    data = obj(r.json())
    return '' + str(len(data.response.song.sampled_songs))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('master.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()

