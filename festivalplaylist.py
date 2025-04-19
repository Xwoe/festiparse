import os
from playlist_creator import PlaylistCreator
from band_parser import BandParser

from log import get_logger

logger = get_logger(__name__)


def fill_playlist(festival, url, playlist_name, txt=""):
    user_name = os.environ["SPOTIFY_USER_NAME"]
    logger.info(f"parsing {url}")
    bp = BandParser(url, festival, txt=txt)
    bands = bp.parse()
    bp.print_bands()
    pc = PlaylistCreator(username=user_name, playlist_name=playlist_name)
    pc.update_playlist(bands)


def main():
    # url = "http://haldernpop.com/line-up-2025/"
    # festival = "haldern"
    # playlist_name = "Haldern 2025"
    # txt = "haldern_2025.txt"
    # fill_playlist(festival, url, playlist_name, txt)

    url = "https://www.maifeld-derby.de/lineup"
    festival = "maifeld"
    playlist_name = "Maifeld Derby 2025"
    txt = "maifeld_2025.txt"
    fill_playlist(festival, url, playlist_name, txt)

    # url = "https://orangeblossomspecial.de/programm/"
    # festival = "obs"
    # playlist_name = "Orange Blossom Special 2024"
    # fill_playlist(festival, url, playlist_name)


if __name__ == "__main__":
    main()
