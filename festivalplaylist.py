import os
from playlist_creator import PlaylistCreator
from band_parser import BandParser

from log import get_logger
logger = get_logger(__name__)


def fill_playlist(festival, url, playlist_name):

    user_name = os.environ['SPOTIFY_USER_NAME']
    logger.info(f'parsing {url}')
    bp = BandParser(url, festival)
    bands = bp.parse()
    pc = PlaylistCreator(username=user_name, playlist_name=playlist_name)
    pc.update_playlist(bands)

def main():

    url = 'http://haldernpop.com/bands/line-up-2019'
    festival = 'haldern'
    playlist_name = 'Haldern 2019'
    fill_playlist(festival, url, playlist_name)

    url = 'http://www.maifeld-derby.de/line-up'
    festival = 'maifeld'
    playlist_name = 'Maifeld Derby 2019'
    fill_playlist(festival, url, playlist_name)

    url = 'https://orangeblossomspecial.de/?page_id=15464'
    festival = 'obs'
    playlist_name = 'Orange Blossom Special 2019'
    fill_playlist(festival, url, playlist_name)
    

if __name__ == "__main__":
    main()