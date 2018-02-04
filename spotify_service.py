import requests
import json
import artist
import song

from credentials import SPOTIFY_KEY
from credentials import SPOTIFY_SECRET
from credentials import USER_ID

#Make the bearer token call up here, so it'll be done when the module is initialized


def get_bearer_token():
    token = ''
    key = SPOTIFY_KEY
    secret = SPOTIFY_SECRET

    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials'}

    print('Getting Spotify token')
    response = requests.post(url, headers=headers, params=payload, auth=(key, secret))
    
    json_data = response.json()
    
    #Now we get the token out of the JSON response
    if('error' not in json_data and 'access_token' in json_data):
        token = json_data['access_token']
    #Need some kind of Else to raise an exception

    print('Spotify token acquired')
    return token

def read_songs_from_playlist(playlist_id):
    headers = {'Authorization': 'Bearer ' + token}

    user_id = USER_ID
    
    print('Calling Spotify for playlist')
    
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists/' + playlist_id
    #Make playlist call with user_id & playlist_id
    response = requests.get(url, headers=headers)
    #Read out songs from response
    json_data = response.json()

    songs = []

    for item in json_data['tracks']['items']:
        track = item['track']
        name = track['name']
        #We'll need to keep track of the spotifyID of these songs too, to create the playlist.
        spotify_id = track['id']
        artist_name = track['artists'][0]['name']
        current_song = song.make_song_with_id(name, artist_name, spotify_id)
        songs.append(current_song)
        
    return songs

def write_playlist(song_list):

    #Create the empty playlist. How do we name it? Do we pass in the original name and modify it?

    #Add a list of songs to the playlist
    return None

token = get_bearer_token()
