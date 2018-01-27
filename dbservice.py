import pyorient
import artist
import json
def _escape(string):
    return string.replace("'","\\'")

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "password")
client.db_open("musicartists", "root", "password")



def init():
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "password")

def get_artists_to_call():
    print('Getting artists')
    query = 'SELECT * FROM ARTIST WHERE called=false'
    database_artists = client.query(query, 100)
    response = []
    for database_artist in database_artists:
        artist_dto = artist.make_artist(database_artist.name)
        response.append(artist_dto)


    return response

def get_artist(artist_to_get):
    query = "SELECT * FROM ARTIST WHERE name = '" + _escape(artist_to_get.name) + "'"
    returned_artists = client.query(query)
    if(returned_artists and returned_artists[0] is not None):
        return returned_artists[0]
    else:
        return None


def insert_new_artist(artist_to_insert):
    #PyOrient has ways to make this an async call. Examine whether we should do this depending on the times.

    query = "INSERT INTO ARTIST SET name = '" + _escape(artist_to_insert.name) + "', called = 0"
    client.command(query)

    print('New Artist: ' + artist_to_insert.name)
    return


def create_new_link(origin_artist, related_artist):
    print('New Link: ' + origin_artist.name + ' to ' + related_artist.name)

    query = "CREATE EDGE similarto FROM (SELECT * FROM ARTIST WHERE name='" + _escape(origin_artist.name) + "') TO (SELECT * FROM ARTIST WHERE name='" + _escape(related_artist.name) + "')"
    client.command(query)

    return

def update_artist_called(artist_to_update):   
    query = "UPDATE ARTIST SET called = 1 where name = '" + _escape(artist_to_update.name) + "'"
    client.command(query)

    return

def get_shortest_path(origin_artist, target_artist):
    query = ("SELECT count(path) FROM ("
             "SELECT shortestPath($from, $to) AS path "
             "LET $from = (SELECT FROM Artist WHERE name='" + _escape(origin_artist.name) + "'), "
             "$to = (SELECT FROM Artist WHERE name='" + _escape(target_artist.name) +
             "') UNWIND path)")

    result = client.query(query)
    if(result and result[0] is not None):
        #Subtracting 1 because shortest_path and traverse count things slightly differently. Keeping it consistent
        return int(result[0].oRecordData['count'])-1
    else:
        return None
    
def traverse(origin_artist, artist_to_traverse):
    query = "SELECT $depth FROM( TRAVERSE out(similarto),in(similarto) FROM (SELECT * FROM ARTIST WHERE name='" + _escape(origin_artist.name) + "') STRATEGY BREADTH_FIRST) where name='" + _escape(artist_to_traverse.name) + "'"
    result = client.query(query)
    if(result and result[0] is not None):
        return int(result[0].oRecordData['$depth'])
    else:
        return None

def seed_db_for_test():
    print('Deleting all values in DB')
    delete_query = "DELETE VERTEX ARTIST"
    client.command(delete_query)

    print('Re-seeding DB with initial values')
    insert_query = "INSERT INTO ARTIST SET name = 'VNV Nation', called = 0"
    client.command(insert_query)

    insert_query = "INSERT INTO ARTIST SET name = 'Alestorm', called = 0"
    client.command(insert_query)

    insert_query = "INSERT INTO ARTIST SET name = 'Metallica', called = 0"
    client.command(insert_query)

    insert_query = "INSERT INTO ARTIST SET name = 'Medwyn Goodall', called = 0"
    client.command(insert_query)

    insert_query = "INSERT INTO ARTIST SET name = '2 Live Crew', called = 0"
    client.command(insert_query)


def close():
    # This actually closes the DB entirely. Maybe good 
    # for the future, but we don't want to do that now.
    client.shutdown('root', 'password')
