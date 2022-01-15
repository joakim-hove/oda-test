from .oda import OdaScraper
from .util import Fetcher
from .product_catalog import ProductCatalog

from bs4 import BeautifulSoup


def parse(text):
    return BeautifulSoup(text, features="html.parser")
