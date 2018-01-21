import requests
import json
import artist

from credentials import LAST_FM_API_KEY

def get_related_artists(artist_to_call):
    name = artist_to_call.name
    key = LAST_FM_API_KEY
    print('Making API call for ' + artist_to_call.name)
    response = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist='+
                            name+'&api_key='+key+'&format=json')
    
    json_data = response.json()
    
    #Now we construct a list of the top ten, and return that. We don't want to return all 100 artists
    response = []
    for i in range(0,10):
        if('error' not in json_data and 'similarartists' in json_data and len(json_data['similarartists']['artist'])>0):
            related_artist = json_data['similarartists']['artist'][i]

    #for related_artist in json_data['similarartists']['artist']:
    #    print(artist.name + ' is similar to ' + related_artist['name'])
            related_artist_dto = artist.make_artist(related_artist['name'], False)
            response.append(related_artist_dto)
    return response
