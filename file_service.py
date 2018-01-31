import csv
import song

FILETYPE = '.csv'


def read_playlist(FILENAME):
    song_list = []
    with open(FILENAME + FILETYPE, 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
        #Make a Song out of each row, add to list
            song_row = song.make_song(row[0], row[1])
            song_list.append(song_row)
    return song_list

def write_playlist(FILENAME, SOLUTION):
    with open(FILENAME + '-solved' + FILETYPE, "w", newline='') as file:
        writer = csv.writer(file, delimiter='|')
        for song_row in SOLUTION:
            writer.writerow([str(song_row), str(song_row.artist.name)])
