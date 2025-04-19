import os
import requests
from bs4 import BeautifulSoup

from log import get_logger

logger = get_logger(__name__)

TAGS = {
    "haldern": ["h4", "list-title"],
    "maifeld": ["a"],
    "obs": ["h2", "entry-title fusion-post-title"],
}

THISDIR = os.path.dirname(os.path.abspath(__file__))


class BandParser:
    def __init__(self, url, festival="haldern", txt=""):
        self.txt = os.path.join(THISDIR, txt)
        self.html_doc = requests.get(url).content
        self.soup = BeautifulSoup(self.html_doc, "html.parser")
        self.festival = festival

    def parse_entries(self):
        if self.txt:
            self.parse_file()
        else:
            self.samples = self.soup.find_all(*TAGS[self.festival])

    def _parse_a(self):
        for s in self.samples:
            a = s.findAll("a")
            a0 = a[0]
            band = a0.string.strip()
            band = band.split(" (")[0]
            self.bands.append(band)

    def _parse_maifeld(self):
        for s in self.samples:
            classes = set(
                [
                    "el-item",
                    "uk-card",
                    "uk-card-primary",
                    "uk-card-hover",
                    "uk-margin-remove-first-child",
                    "uk-transition-toggle",
                    "uk-link-toggle",
                    "uk-display-block",
                ]
            )
            actual_classes = s.attrs.get("class")
            if actual_classes:
                actual_classes = set(s.attrs.get("class"))
                if actual_classes == classes:
                    band = s.attrs.get("aria-label")
                    self.bands.append(band)

    def parse_html_samples(self):
        if self.txt:
            return

        self.bands = []
        if self.festival == "maifeld":
            self._parse_maifeld()
            self._parse_a()
        else:
            # temporary fix for Haldern
            self._parse_a()

    def parse_file(self):
        self.bands = []
        with open(self.txt, "r") as file:
            for line in file.readlines():
                band = line.strip()
                band = band.split(" (")[0]
                self.bands.append(band)

    def print_bands(self):
        for band in self.bands:
            # logger.info(band)
            print(band)

    def parse(self):
        self.parse_entries()
        self.parse_html_samples()
        return self.bands
