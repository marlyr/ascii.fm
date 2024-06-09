from dotenv import load_dotenv
import argparse
import os
import requests
import sys
from ascii_magic import AsciiArt, from_image

load_dotenv()

API_KEY = os.getenv('API_KEY')
USER_AGENT = 'Test'

def lastfm_get(method, username=None, album=None, artist=None, limit=None, autocorrect=None):
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload = {
        'method': method,
        'api_key': API_KEY,
        'format': 'json'
    }
    
    if username:
        payload['user'] = username
    if album:
        payload['album'] = album
    if artist:
        payload['artist'] = artist
    if limit:
        payload['limit'] = limit
    if autocorrect:
        payload['autocorrect'] = autocorrect

    response = requests.get(url, headers=headers, params=payload)
    return response


def check_user(username):
    method = 'user.getInfo'
    response = lastfm_get(method, username=username)
    if response.status_code != 200:
        sys.exit('Invalid username')

def get_recentTrack(username, limit=1):
    method = 'user.getRecentTracks'
    response = lastfm_get(method, username=username, limit=limit)
    data = response.json()

    try:
        track = data['recenttracks']['track'][0]
        return track['name'], track['artist']['#text'], track['image'][1]['#text']
    except (IndexError, KeyError):
        sys.exit('No recent tracks.')


def albumSearch(album, limit=1):
    method = 'album.Search'
    response = lastfm_get(method, album=album, limit=limit)
    data = response.json()

    try:
        release = data['results']['albummatches']['album'][0]
        return release['name'], release['artist'], release['image'][1]['#text']
    except IndexError:
        sys.exit('Album not found.')
    

def get_topAlbum(artist, limit=1, autocorrect=1):
    method = 'artist.getTopAlbums'
    response = lastfm_get(method, artist=artist, limit=limit, autocorrect=autocorrect)
    data = response.json()

    try:
        release = data['topalbums']['album'][0]
        return release['name'], release['artist']['name'], release['image'][1]['#text']
    except (KeyError, ValueError):
        sys.exit('Artist not found.')

def get_albumArtist(album, artist, autocorrect=1):
    method = 'album.getInfo'
    album = ' '.join(album)
    artist = ' '.join(artist)
    response = lastfm_get(method, album=album, artist=artist, autocorrect=autocorrect)

    data = response.json()
    
    try:
        release = data['album']
        return release['name'], release['artist'], release['image'][1]['#text']
    except (KeyError, ValueError):
        sys.exit('Album not found.')


def display_album_art(username=None, album=None, artist=None):
    if username:
        check_user(username)
        album, artist, image = get_recentTrack(username)
    elif album:
        if artist:
            album, artist, image = get_albumArtist(album, artist)
        else:
            album, artist, image = albumSearch(album)
    elif artist:
        album, artist, image = get_topAlbum(artist)
    
    print(f'{album} by {artist}')
    print()
    try:
        art = AsciiArt.from_url(image)
        art.to_terminal(columns=80)
    except ValueError:
        sys.exit('Album not found.')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A command-line interface for exploring Last.fm music data.')
    parser.add_argument('-u', '--username', type=str, help='Specify Last.fm username to display most recently played track.', required=False, dest='username')
    parser.add_argument('-a', '--album', type=str, nargs='+', help='Specify album name in quotes. Use --artist to refine search.', required=False, dest='album')
    parser.add_argument('-r', '--artist', type=str, nargs='+', help='Specify artist\'s name in quotes. Use --album to refine search.', required=False, dest='artist')

    args = parser.parse_args()
    if not (args.username or args.album or args.artist):
        parser.print_help()
        sys.exit()

    display_album_art(args.username, args.album, args.artist)
