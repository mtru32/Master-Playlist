import config
import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

userId = ''
playlistId = ''
sp = None

def auth():
    scope = "user-library-read, playlist-modify-public"
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_secret=config.SPOTIPY_CLIENT_SECRET, client_id=config.SPOTIPY_CLIENT_ID, scope=scope, redirect_uri=config.ruri))

def get_songs():
    all_songs = []
    results = sp.current_user_playlists()
    global userId
    userId = results['items'][0]['owner']['id'] # Save Id for create_playlist()
    for item in results['items']:
        playlist = sp.playlist(item['id'])
        tracklist = playlist['tracks']['items']
        for song in tracklist:
            song_id = song['track']['id']
            if song_id not in all_songs:
                all_songs.append(song_id)
    return all_songs

def create_playlist():
    new_playlist = sp.user_playlist_create(userId, 'All Songs', public=True, collaborative=False, description='')
    global playlistId
    playlistId = new_playlist['id'] # save newly created playlist Id

def add_songs(all_songs):
    random.shuffle(all_songs)
    if (len(all_songs) > 100): # spotify allows only 100 songs per request
        n = 100
        split_songs = [all_songs[i:i+n] for i in range(0, len(all_songs), n)]
        for songs in split_songs:
            sp.playlist_add_items(playlistId, songs)
    else:
        sp.playlist_add_items(playlistId, all_songs)

def main():
    auth()
    all_songs = get_songs()
    create_playlist()
    add_songs(all_songs)
    os.remove('.cache')

if __name__ == '__main__':
    main()