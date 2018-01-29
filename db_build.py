import sys
import time
import dbservice
import musicservice


def call_api_for_list(artists_to_call):
    time_of_last_api_call = time.time()
    counter = 0
    for artist in artists_to_call:
        #One call per second to avoid pissing off LastFM
        print(str(counter) + ' calls performed')
        if time.time() - time_of_last_api_call < 1:
            print(str(time.time() - time_of_last_api_call) + ' seconds elapsed. Extra sleep.')
            time.sleep(1)
        #Hit the API
        related_artists = musicservice.get_related_artists(artist)
        time_of_last_api_call = time.time()

        #Now we persist any new artists and add them to the artists_to_call list
        for related_artist in related_artists:
            #If this artist is NOT in the DB, insert them into the DB and add them to the list
            if not dbservice.get_artist(related_artist):
                dbservice.insert_new_artist(related_artist)
            #Now we persist edges between the artist called and this related artist
            dbservice.create_new_link(artist, related_artist)

        #Update artist to called in the DB
        dbservice.update_artist_called(artist)
        counter += 1


def main():
    #Re-seeding from scratch for testing purposes
    #dbservice.seed_db_for_test()


    if len(sys.argv) >= 2:
        NUMBER_OF_ARTISTS = int(sys.argv[1])
    else:
        #Default 100, put in arguments for more
        NUMBER_OF_ARTISTS = 10
    #Call the database for the number of artists that need to be called
    ARTISTS_TO_CALL = dbservice.get_artists_to_call(NUMBER_OF_ARTISTS)

    print('Making ' + str(NUMBER_OF_ARTISTS) + ' API calls')

    call_api_for_list(ARTISTS_TO_CALL)

    print('Maximum number of iterations reached. Aborting.')



if __name__ == "__main__":
    main()