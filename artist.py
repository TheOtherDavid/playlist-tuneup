class Artist(object):
    name = ''
    mbid = ''

    def __init__(self, name):
        self.name=name

        #Not using mbid for now
        #self.mbid=mbid

    def __eq__(self, obj):
        return isinstance(obj, Artist) and obj.name == self.name

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return self.name
    

def make_artist(name):
    artist = Artist(name)
    return artist
