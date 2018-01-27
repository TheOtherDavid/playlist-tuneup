import math
import time
import collections
import dbservice

from collections import defaultdict



def nearest_neighbors(song_list):
    #Do nearest neighbor algo once with each song as the lead song
    best_solution = []
    best_distance = math.inf
    artist_dict = find_all_distances(song_list)
    for first_song in song_list:
        time_of_solution = time.time()

        #print('First song is: ' + str(first_song))
        unplayed_songs = song_list.copy()
        unplayed_songs.remove(first_song)
        played_songs = [first_song]
        current_distance = 0

        while unplayed_songs:
            #Figure out next song by figuring out the closest song from unplayed
            #Get a list of all the possible transitions? Lot of DB calls...
            #Should we pre-construct a matrix?

            #min(of the possible transitions from latest played to each of unplayed)
            distances = []

            for unplayed_song in unplayed_songs:
                #Find the difference between the current song and the last song and add it to a list

                distance = artist_dict[played_songs[-1].artist][unplayed_song.artist]

                distances.append(distance)
            #Next song is the minimum of the distances
            min_distance = min(distances)
            min_distance_song = unplayed_songs[distances.index(min(distances))]
            #print('Minimum distance song is ' + min_distance_song.name + ' with a distance of ' + str(min_distance))
            next_song = min_distance_song
            #print('Next song is: ' + next_song.name)
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
    #So we need to get all the distances and put them into a multidimensional dict.
    #Start by calling get_shortest_path for each combo? We'll work on the combo call later.
    artist_dict = defaultdict(dict)
    time_start = time.time()

    print('Building artist dictionary.')

    for song_from in song_list:
        for song_to in song_list:
            if song_from.artist != song_to.artist:
                distance = dbservice.get_shortest_path(song_from.artist, song_to.artist)
                artist_dict[song_from.artist][song_to.artist] = distance
    print('Building artist dictionary took '  + str(time.time() - time_start))
    return artist_dict
