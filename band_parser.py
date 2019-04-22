import requests
from bs4 import BeautifulSoup

from log import get_logger
logger = get_logger(__name__)

TAGS = {'haldern': ["h4", "list-title"],
        'maifeld': ["figure", "wk-overlay wk-overlay-hover "],
        'obs': ["h2", "entry-title fusion-post-title"]}

class BandParser():

    def __init__(self, url, festival='haldern'):
        self.html_doc = requests.get(url).content
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        self.festival = festival

    def parse_entries(self):
        self.samples = self.soup.find_all(*TAGS[self.festival])

    def _parse_a(self):
        for s in self.samples:
            a = s.findAll('a')
            a0 = a[0]
            band = a0.string.strip()
            band = band.split(' (')[0]
            self.bands.append(band)

    def _parse_maifeld(self):
        
        for s in self.samples:

            result_all = s.findAll('img')
            for item in result_all:
                if 'alt' in item.attrs.keys():
                    band = item.attrs['alt']

            band = band.split('(')[0]
            band = band.strip()
            self.bands.append(band)

    def parse_samples(self):
        self.bands = []
        
        if self.festival == 'maifeld':
            self._parse_maifeld()
        else:
            self._parse_a()

    def print_bands(self):
        for band in self.bands:
            logger.info(band)

    def get_bands(self):
        return self.bands

    def parse(self):
        self.parse_entries()
        self.parse_samples()
        return self.get_bands()
