import sys
import time
import song
import algorithm
import file_service

START_TIME = time.time()
#Testing arguments
if len(sys.argv) >= 2:
    FILENAME = sys.argv[1]
    print('Argument ' + str(sys.argv[1]) + ' was provided.')
else:
    FILENAME = 'playlist-test'

SONG_LIST = file_service.read_playlist(FILENAME)

for song in SONG_LIST:
    #Print the Songs from the Song object
    print(song.name + ' by ' + song.artist.name)

SOLUTION = algorithm.nearest_neighbors(SONG_LIST)

print('Solution found:')
print(', '.join(str(x) for x in SOLUTION))

file_service.write_playlist(FILENAME, SOLUTION)

print('Full solution took ' + str(time.time()-START_TIME))
