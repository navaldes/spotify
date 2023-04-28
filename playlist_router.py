from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pprint import pprint
from setup import RestSetup
from models import links
import backend as b


router = APIRouter()


@router.post('/song/find', tags=['Playlist'])
def find_song_in_playlists(user_input: links):
    rest = RestSetup()

    headers = rest.get_headers()

    url = 'https://api.spotify.com/v1/'

    b.validate_links(user_input.user_link, user_input.song_link)

    # Get User ID
    # user_link = input("Paste profile link: ")
    user_id = b.get_user_id(user_input.user_link)

    # Get Users Playlists
    users_playlists = b.get_users_playlists(user_id, url, headers)
    b.display_users_playlist(users_playlists)

    # Get all playlists songs
    playlists = b.get_playlists_songs(users_playlists, url, headers)
    b.display_playlists(playlists)

    # Get Song ID
    # song_link = input('Paste song link: ')
    song_id = b.get_song_id(user_input.song_link)

    # Search for song in all playlists
    playlists_with_song = b.find_playlist_song_exists(playlists, song_id)
    if playlists_with_song:
        song_list = ', '.join(playlists_with_song)
        msg = f'Song found in the following playlists: {song_list}'
    else:
        msg = 'Song not found in any playlists'

    return JSONResponse(content={'message': msg}, status_code=200)