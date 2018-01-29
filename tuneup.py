import sys
import csv
import time
import song
import artist
import algorithm

start_time = time.time()
#Testing arguments
if len(sys.argv) >= 2:
    arg = int(sys.argv[1])
    print('Argument ' + str(sys.argv[1]) + ' was provided.')

#TODO: Pass in the name of the CSV file as an argument

#Testing read CSV
FILENAME = 'trimmed-playlist'
FILETYPE = '.csv'
song_list = []
with open(FILENAME + FILETYPE, 'r') as file:
    READER = csv.reader(file, delimiter='|')
    for row in READER:
    #Make a Song out of each row, add to list
        song_row = song.make_song(row[0], row[1])
        song_list.append(song_row)

for song in song_list:
    #Print the Songs from the Song object
    print(song.name + ' by ' + song.artist.name)

SOLUTION = algorithm.nearest_neighbors(song_list)

print('Solution found:')
print(', '.join(str(x) for x in SOLUTION))
print('Full solution took ' + str(time.time()-start_time))

#TODO: write a new CSV file with the properly-ordered solution

with open(FILENAME + '-solved' + FILETYPE, "w", newline='') as file:
    WRITER = csv.writer(file, delimiter='|')
    for song in SOLUTION:
        WRITER.writerow([str(song), str(song.artist.name)])
