import artist

class Song(object):
    name = ''

    def __init__(self, name, artist, spotify_id = None):
        self.name=name

        #Not using mbid for now
        #self.mbid=mbid

        self.artist=artist
        self.spotify_id = spotify_id

    def __eq__(self, obj):
        return isinstance(obj, Song) and obj.name == self.name

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return self.name


def make_song(name, artist_name):
    song = Song(name, artist.make_artist(artist_name))
    return song

def make_song_with_id(name, artist_name, spotify_id):
    song = Song(name, artist.make_artist(artist_name), spotify_id)
    return song