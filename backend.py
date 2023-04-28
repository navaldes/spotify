import requests
from fastapi import HTTPException
from pprint import pprint

def validate_links(user_link, song_link):
    print('Validating links')
    try:
        user_id_list = user_link.split('/')
        if user_id_list[-2] != 'user':
            raise HTTPException(detail=f"'{user_link}' is not a user link", status_code=500)
    except IndexError:
        raise HTTPException(detail=f"'{user_link}' is not a valid link", status_code=500) 
    
    print('User link valid')
    try:
        song_id_list = song_link.split('/')
        if song_id_list[-2] != 'track':
            raise HTTPException(detail=f"'{song_link}' is not a song link", status_code=500)
    except IndexError:
        raise HTTPException(detail=f"'{song_link}' is not a valid link", status_code=500)
    
    print('Song link valid')
    print('All links valid')
    return


def get_user_id(user_link):
    user_id_list = user_link.split('/')
        
    user_id = user_id_list[-1].split('?')[0]

    return user_id

def get_users_playlists(user_id, BASE_URL, headers):
    print('Getting Users Playlist...')

    # requests to get playlists of user
    r = requests.get(BASE_URL + f'users/{user_id}/playlists', headers=headers, params={})

    response = r.json()

    user_playlists = []

    # add playlist names and id to list

    for item in response['items']:
        user_playlists.append({'name': item['name'],
                               'id': item['id']})
        
    while response['next']:
        r = requests.get(response['next'], headers=headers, params={})

        response = r.json()
        
        for item in response['items']:
            user_playlists.append({'name': item['name'],
                                'id': item['id']})
            
    return user_playlists

def display_users_playlist(users_playlists):

    print(f'\nFound {len(users_playlists)} public playlist(s)')

    return

def get_playlists_songs(user_playlists, BASE_URL, headers):
    print("\nGetting songs from all playlists...")

    playlists = []

    # for each playlist call GET request to get songs then add each playlist and its songs to a list
    for playlist in user_playlists:
        playlist_id = playlist['id']

        r = requests.get(BASE_URL + f'playlists/{playlist_id}/tracks', headers=headers, params={})

        playlist_response = r.json()
        
        # pprint(playlist_response)
        songs = {}

        # add each song to songs list
        for song in playlist_response['items']:
            if song['track'] is not None:
                songs[song['track']['id']] = song['track']['name']

        # api has a return limit so ['next'] is the url to the next songs in the list, returns null if no more songs
        while playlist_response['next']:
            r = requests.get(playlist_response['next'], headers=headers, params={})

            playlist_response = r.json()

            for song in playlist_response['items']:
                if song['track'] is not None:
                    songs[song['track']['id']] = song['track']['name']

        # once all songs are in songs list, add map of playlist name and songs to playlist list
        playlists.append({'name': playlist['name'],
                        'songs': songs})
        
    return playlists

def display_playlists(playlists):
    print('Displaying Users Playlist...')
    for playlist in playlists:
        print('Playlist Name: {playlist_name}, Song Count: {song_count}'.format(playlist_name=playlist['name'], song_count=len(playlist['songs'])))

    return

def get_song_id(song_link):
    
    song_id_list = song_link.split('/')
        
    song_id = song_id_list[-1].split('?')[0]

    return song_id

def find_playlist_song_exists(playlists, song_id):
    print(f'Searching for song in users playlists...')

    playlists_with_song = []

    for playlist in playlists:
        if song_id in playlist['songs']:
            playlists_with_song.append(playlist['name'])
    
    return playlists_with_song