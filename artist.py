class Artist(object):
    name = ''
    mbid = ''

    called = 0

    def __init__(self, name, called):
        self.name=name

        #Not using mbid for now
        #self.mbid=mbid
        self.called=called

    def __eq__(self, obj):
        return isinstance(obj, Artist) and obj.name == self.name

    def __ne__(self, obj):
        return not self==obj

def make_artist(name,called):
    artist = Artist(name,called)
    return artist
