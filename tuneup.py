import sys
import time
import dbservice
import musicservice

#Re-seeding from scratch for testing purposes

#dbservice.seed_db_for_test()

#First we access the database and get some artist that need to be called
artists_to_call = dbservice.get_artists_to_call()
master_counter = 0
if len(sys.argv) >= 2:
    max_counter = int(sys.argv[1])
else:
    max_counter = 300

#Then we split that into two lists, called and toCall
print('Making ' + str(max_counter) + ' API calls')

time_of_last_api_call = time.time()

#Then we hit the LastFM API

for artist in artists_to_call:
    print(str(master_counter) + ' artists called.')
    if master_counter >= max_counter:
        print('Maximum number of iterations reached. Aborting.')
        break
    #One call per second to avoid pissing off LastFM
    if time.time() - time_of_last_api_call < 1:
        print(str(time_of_last_api_call - time.time()) + ' seconds elapsed. Extra sleep.')
        time.sleep(1)
    related_artists = musicservice.get_related_artists(artist)
    
    time_of_last_call = time.time


    #Now we persist any new artists and add them to the artists_to_call list
    for related_artist in related_artists:
        #If this artist is NOT in the DB, insert them into the DB and add them to the list
        if not dbservice.get_artist(related_artist):
        #if(related_artist not in called_artists and related_artist not in artists_to_call):
            dbservice.insert_new_artist(related_artist)
            #Not adding it to the current list anymore. This will help flesh out current DB.
            #artists_to_call.append(related_artist)


    #Now we persist any new edges
        dbservice.create_new_link(artist, related_artist)

    #Update artist to called in the DB
    dbservice.update_artist_called(artist)

    master_counter = master_counter + 1





#Then we persist all new edges

#Then we close the DB connection?
#db.close()
