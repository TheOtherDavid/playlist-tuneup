import pyorient
import artist
import json

from credentials import ORIENT_USER_ID
from credentials import ORIENT_PASSWORD

def _escape(string):
    return string.replace("'","\\'")

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect(ORIENT_USER_ID, ORIENT_PASSWORD)
if client.db_exists("MusicArtists"):
    client.db_open("MusicArtists", ORIENT_USER_ID, ORIENT_PASSWORD)
    print('Connected to database MusicArtists')
else:
    print('Database MusicArtists not found. Creating database.')
    client.db_create("MusicArtists")
    client.db_open("MusicArtists", ORIENT_USER_ID, ORIENT_PASSWORD)
    create_artist_query = 'CREATE CLASS ARTIST EXTENDS V'
    client.command(create_artist_query)
    create_similar_to_query = 'CREATE CLASS SIMILARTO EXTENDS E'
    client.command(create_similar_to_query)

    



def init():
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "password")

def get_artists_to_call(number_of_artists):
    print('Getting artists')
    query = 'SELECT * FROM ARTIST WHERE called = 0'
    database_artists = client.query(query, number_of_artists)
    response = []
    for database_artist in database_artists:
        artist_dto = artist.make_artist(database_artist.name)
        response.append(artist_dto)


    return response

def get_artist(artist_to_get):
    """Gets an artist from the database.
    Input: Artist object
    Output: Artist object, or None if artist not found"""
    query = "SELECT * FROM ARTIST WHERE name = '" + _escape(artist_to_get.name) + "'"
    returned_artists = client.query(query)
    if(returned_artists and returned_artists[0] is not None):
        return returned_artists[0]
    else:
        return None

def get_uncalled_related_artists_at_depth(artist_to_get, depth):
    query = ("SELECT * FROM (TRAVERSE out(similarto),in(similarto) FROM ("
             "SELECT * FROM ARTIST WHERE name='" + _escape(artist_to_get.name) +
             "') MAXDEPTH " + str(depth) + " ) WHERE called = 0")
    database_artists = client.query(query)
    response = []
    for database_artist in database_artists:
        artist_dto = artist.make_artist(database_artist.name)
        if artist_dto not in response:
            response.append(artist_dto)
    return response


def insert_new_artist(artist_to_insert):
    #PyOrient has ways to make this an async call. Examine whether we should do this depending on the times.

    query = "INSERT INTO ARTIST SET name = '" + _escape(artist_to_insert.name) + "', called = 0"
    client.command(query)

    print('New Artist: ' + artist_to_insert.name)
    return


def create_new_link(origin_artist, related_artist):
    print('New Link: ' + origin_artist.name + ' to ' + related_artist.name)

    query = "CREATE EDGE SIMILARTO FROM (SELECT * FROM ARTIST WHERE name='" + _escape(origin_artist.name) + "') TO (SELECT * FROM ARTIST WHERE name='" + _escape(related_artist.name) + "')"
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
        return int(result[0].oRecordData['count'])
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
