# rapgraph
Trying out Flask and Python, with Relay and GraphQL support!

You probably want to use virtualenv and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
```shell
git clone https://github.com/jahrlin/rapgraph
cd rapgraph
pip install -r requirements.txt
python server.py & open http://localhost:5000
```

## Instructions
If you want to add songs to the db:
* Get a Genius API token
* Set up a firebase db with a root node called `songs`
* Set token and db url in server.py

Add new songs at http://localhost:5000/songs/add/<id>

Currently just showing edges for songs and their samples/samplings
