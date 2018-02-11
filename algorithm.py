import math
import time
from collections import defaultdict
import dbservice
import db_build

def nearest_neighbors(song_list):
    """Solves the optimization problem for the most efficient order of the list.
    Input: List of songs
    Output: Reordered list of songs
    """

    verify_and_add_artists(song_list)
    #Build matrix of distances between artists
    artist_dict = find_all_distances(song_list)

    best_solution = []
    best_distance = math.inf
    #Do nearest neighbor algo once with each song as the lead song, pick best
    for first_song in song_list:
        time_of_solution = time.time()

        #print('First song is: ' + str(first_song))
        unplayed_songs = song_list.copy()
        unplayed_songs.remove(first_song)
        played_songs = [first_song]
        current_distance = 0

        while unplayed_songs:
            #Figure out next song by figuring out the closest song from unplayed
            distances = []

            for unplayed_song in unplayed_songs:
                #Find the difference between the current song and the last song and add it to a list
                distance = artist_dict[played_songs[-1].artist][unplayed_song.artist]

                distances.append(distance)

            #Next song is the song with the minimum distance
            min_distance = min(distances)
            next_song = unplayed_songs[distances.index(min_distance)]

            current_distance = current_distance + min_distance
            played_songs.append(next_song)
            unplayed_songs.remove(next_song)
        print(', '.join(str(x) for x in played_songs))
        print('Feasible solution with total distance ' + str(current_distance))
        print('Solution took ' + str(time.time() - time_of_solution))
        if current_distance < best_distance:
            best_solution = played_songs
            best_distance = current_distance

    return best_solution


def find_all_distances(song_list):
    """Builds a matrix of distances between each pair of artists in song list.
    Input: List of song objects
    Output: Two-dimensional dictionary with artists as keys and distances as values"""
    #So we need to get all the distances and put them into a multidimensional dict.
    #Start by calling get_shortest_path for each combo? We'll work on the combo call later.
    artist_dict = defaultdict(dict)
    time_start = time.time()

    print('Building artist dictionary')
    for song_from in song_list:
        #Double for-loop to compare each song to each other song
        for song_to in song_list:
            if song_from.artist != song_to.artist:
                #Try to find a path between artists.

                distance = dbservice.get_shortest_path(song_from.artist, song_to.artist)

                if distance == 0:
                    print('Artist not linked to bulk of database. Adding links.')
                    link_artist_to_database(song_from.artist, song_to.artist)
                    print('Artist successfully linked to database')
                    distance = dbservice.get_shortest_path(song_from.artist, song_to.artist)

                artist_dict[song_from.artist][song_to.artist] = distance
            else:
                #If both artists are the same just make it zero. Come up with a better solution later.
                artist_dict[song_from.artist][song_to.artist] = 0
    print('Building artist dictionary took '  + str(time.time() - time_start))
    return artist_dict

def link_artist_to_database(origin_artist, target_artist):
    """When an artist is found to not be linked to another artist, this function
    will call the db-build function to connect the artists."""

    #While loop: While shortest_path not found, get all related artist at a certain depth,
    #and make API calls for those artists. This could take a while, but a link SHOULD be found.
    depth = 1
    while True:
        #Break if shortest path is not 0, IE if a link is found
        if dbservice.get_shortest_path(origin_artist, target_artist) != 0:
            break
        print('Making API calls for depth ' + str(depth))
        artists_to_call = dbservice.get_uncalled_related_artists_at_depth(origin_artist, depth)
        artists_to_call.extend(dbservice.get_uncalled_related_artists_at_depth(target_artist, depth))          

        db_build.add_related_artists_for_list(artists_to_call)
        depth += 1


def verify_and_add_artists(song_list):
    for song in song_list:
        artist = dbservice.get_artist(song.artist)
        if artist is None:
            print("Artist " + song.artist.name + " not found, adding to database.")
            dbservice.insert_new_artist(song.artist)
            db_build.add_related_artists_for_list([song.artist])
