import os
import sys
import json
import spotipy
import webbrowser
import requests

from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import spotipy.util as util
from json.decoder import JSONDecodeError

from log import get_logger
logger = get_logger(__name__)

class PlaylistCreator():

    def __init__(self, username, playlist_name):
        self.username = username
        self.playlist_name = playlist_name
        self.playlist_tracks = []
        self.playlist_description = ''
        self.client_id = os.environ['SPOTIPY_CLIENT_ID']
        self.client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        self.redirect_uri=os.environ['SPOTIPY_REDIRECT_URI']
        self.scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-private playlist-read-private'
        self.set_token()
        self.spotify = spotipy.Spotify(auth=self.token)
        self.playlist_id = self.get_or_create_playlist()

    def set_token(self):
        logger.info('#'*10 + ' ' + self.playlist_name + ' ' + '#'*10)
        try:
            self.token = util.prompt_for_user_token(username=self.username, scope=self.scope, 
                                                    redirect_uri=self.redirect_uri)
        except (AttributeError, JSONDecodeError):
            logger.info('except')
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(username=self.username, scope=self.scope, 
                                                    redirect_uri=self.redirect_uri)


    def get_artist_obj(self, artist):
        results = self.spotify.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            for item in items:
                if item['name'].lower() == artist.lower():
                    artist = item
                    logger.info(artist['name'])
                    return artist
        logger.warning(f'/!\ {artist} >>>> no artist found')
        return ''

    def get_all_playlist_tracks(self, playlist_id):
      
        stepsize = 100
        i = 0
        
        items = self.spotify.user_playlist_tracks(self.username, playlist_id, offset=0, fields=None, limit=stepsize)['items']
        while len(items) > 0:
            self.playlist_tracks += [track['track']['id'] for track in items]
            i += 1
            items = self.spotify.user_playlist_tracks(self.username, playlist_id, offset=i*stepsize,
                                                    fields=None, limit=stepsize)['items']
                    
        
    
    def get_or_create_playlist(self):

        pls = self.spotify.user_playlists(self.username)
        for item in pls['items']:
            if item['name'] == self.playlist_name:          
                self.get_all_playlist_tracks(item['id'])
                return item['id']
        
        # else: create new playlist
        return self.spotify.user_playlist_create(self.username, self.playlist_name,
                        self.playlist_description)['id']


    def get_album_tracks(self, artist_obj):
        results = self.spotify.artist_albums(artist_obj['uri'], album_type='album')
        if len(results['items']) == 0:
            return []
        album_uri = results['items'][0]['uri']
        album_tracks = self.spotify.album_tracks(album_uri)
        
        album_tracks = [track['id'] for track in album_tracks['items']]
        return album_tracks

    def get_top_tracks(self, artist_obj):
        top_tracks = self.spotify.artist_top_tracks(artist_obj['uri'])
        top_tracks = [track['id'] for track in top_tracks['tracks']]
        return top_tracks

    def add_tracks(self, album_tracks, artist):
        """
        Create the list of tracks to add, which are not yet in the playlist.
        """
        
        if self.playlist_tracks:
            add_tracks = [track for track in album_tracks if track not in self.playlist_tracks]
        else:
            add_tracks = album_tracks
        if len(add_tracks) > 0:
            self.spotify.user_playlist_add_tracks(self.username, self.playlist_id, add_tracks, position=None)
            logger.info(f'+++ Tracks added for {artist}')
        
    def update_playlist(self, artists):
        logger.info(f'updating {self.playlist_name}')
        for artist in artists:
            artist_obj = self.get_artist_obj(artist)
            if not artist_obj:
                continue
            album_tracks = self.get_album_tracks(artist_obj)
            if not album_tracks:
                album_tracks = self.get_top_tracks(artist_obj)
                if not album_tracks:
                    logger.warning(f'/!\ nothing found for {artist}')
                    continue
            self.add_tracks(album_tracks, artist)
