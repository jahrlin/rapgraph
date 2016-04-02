from firebase import firebase


data = {}


def setup(db, token):
    global data

    from schema import Artist, Song

    fb = firebase.FirebaseApplication(
                    db,
                    None)

    songs = {}

    dbSongs = fb.get('/songs', None)
    i = 1
    for songId in dbSongs:
        song = dbSongs[songId]
        artists = []
        artists.append(Artist(
            id=song['primary_artist']['id'],
            name=song['primary_artist']['name']
            ))

        sampledsongs = []
        if 'sampled_songs' in song.keys():
            for sample in song['sampled_songs']:
                newsample = Song(
                        id=sample['id'],
                        title=sample['title']
                        )

                sampledsongs.append(newsample)

        samplingsongs = []
        if 'sampling_songs' in song.keys():
            for sampling in song['sampling_songs']:
                newsampling = Song(
                        id=sampling['id'],
                        title=sampling['title']
                        )

                samplingsongs.append(newsampling)

        newsong = Song(
            id=song['id'],
            title=song['title'],
            url=song['url'],
            primaryartist=artists,
            sampledsongs=sampledsongs,
            samplingsongs=samplingsongs
            )

        songs[str(i)] = newsong
        i += 1

    data = songs

    return data


def get_artist(_id):
    return data['Artist'][_id]


def get_song(_id):
    return data['Song'][_id]


def get_artists():
    return data['Artist']


def get_songs():
    return data
