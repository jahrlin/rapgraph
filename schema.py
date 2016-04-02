import graphene
from graphene import relay, resolve_only_args
from data import get_song, get_artist, get_songs, get_artists

schema = graphene.Schema()


class Artist(relay.Node):
    name = graphene.String()
    url = graphene.String()
    image_url = graphene.String()

    @classmethod
    def get_node(cls, id, info):
        return get_artist(id)


class Song(relay.Node):
    title = graphene.String()
    url = graphene.String()
    header_image_url = graphene.String()
    primaryartist = relay.ConnectionField(Artist)
    song_art_image_url = graphene.String()
    featured_artists = relay.ConnectionField(Artist)
    producer_artist = relay.ConnectionField(Artist)
    writer_artists = relay.ConnectionField(Artist)
    release_date = graphene.String()
    sampledsongs = relay.ConnectionField('Song')
    samplingsongs = relay.ConnectionField('Song')

    @classmethod
    def get_node(cls, id, info):
        return get_song(id)


class Query(graphene.ObjectType):
    node = relay.NodeField()
    songs = relay.ConnectionField(Song)

    @resolve_only_args
    def resolve_artists(self):
        print('resolve artists')
        return get_artists()

    @resolve_only_args
    def resolve_songs(self):
        zongs = get_songs()
        dalist = list(zongs.values())
        return dalist


schema.query = Query

