import os
import sys
import requests
import argparse
from dotenv import load_dotenv
from ascii_magic import AsciiArt

class LastFMClient:
    USER_AGENT = 'ascii.fm'

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://ws.audioscrobbler.com/2.0/'
        self.headers = {'user-agent': self.USER_AGENT}

    def _get(self, method, **params):
        payload = {
            'method': method,
            'api_key': self.api_key,
            'format': 'json'
        }
        payload.update(params)
        response = requests.get(self.base_url, headers=self.headers, params=payload)
        return response

    def check_user(self, username):
        method = 'user.getInfo'
        response = self._get(method, user=username)
        if response.status_code != 200:
            sys.exit('Invalid username.')

    def get_recentTrack(self, username, limit=1):
        method = 'user.getRecentTracks'
        response = self._get(method, username=username, limit=limit)
        data = response.json()

        try:
            track = data['recenttracks']['track'][0]
            return track['name'], track['artist']['#text'], track['image'][1]['#text']
        except (IndexError, KeyError):
            sys.exit('No recent tracks.')

    def albumSearch(self, album, limit=1):
        method = 'album.Search'
        response = self._get(method, album=album, limit=limit)
        data = response.json()

        try:
            release = data['results']['albummatches']['album'][0]
            return release['name'], release['artist'], release['image'][1]['#text']
        except IndexError:
            sys.exit('Album not found.')

    def get_topAlbum(self, artist, limit=1, autocorrect=1):
        method = 'artist.getTopAlbums'
        response = self._get(method, artist=artist, limit=limit, autocorrect=autocorrect)
        data = response.json()

        try:
            release = data['topalbums']['album'][0]
            return release['name'], release['artist']['name'], release['image'][1]['#text']
        except (KeyError, ValueError):
            sys.exit('Artist not found.')

    def get_albumArtist(self, album, artist, autocorrect=1):
        method = 'album.getInfo'
        album = ' '.join(album)
        artist = ' '.join(artist)
        response = self._get(method, album=album, artist=artist, autocorrect=autocorrect)

        data = response.json()
        
        try:
            release = data['album']
            return release['name'], release['artist'], release['image'][1]['#text']
        except (KeyError, ValueError):
            sys.exit('Album not found.')


def main():
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        sys.exit('API_KEY not found.')
    args = get_args()
    client = LastFMClient(API_KEY)
    display_album_art(client, args.username, args.album, args.artist)


def get_args():
    parser = argparse.ArgumentParser(description='A command-line tool for displaying album art from last.fm music data.')
    parser.add_argument('-u', '--username', type=str, help='Specify Last.fm username to display most recently played track.', required=False, dest='username')
    parser.add_argument('-a', '--album', type=str, nargs='+', help='Specify album name in quotes. Use --artist to refine search.', required=False, dest='album')
    parser.add_argument('-r', '--artist', type=str, nargs='+', help='Specify artist\'s name in quotes. Use --album to refine search.', required=False, dest='artist')

    args = parser.parse_args()
    if not (args.username or args.album or args.artist):
        parser.print_help()
        sys.exit()
    
    return args


def display_album_art(client, username=None, album=None, artist=None):
    if username:
        client.check_user(username)
        album, artist, image = client.get_recentTrack(username)
    elif album:
        if artist:
            album, artist, image = client.get_albumArtist(album, artist)
        else:
            album, artist, image = client.albumSearch(album)
    elif artist:
        album, artist, image = client.get_topAlbum(artist)
    
    try:
        art = AsciiArt.from_url(image)
        print(f'{album} by {artist}')
        print()
        art.to_terminal(columns=80)
    except ValueError:
        sys.exit('Album image not found.')


if __name__ == '__main__':
   main()