import datetime
import pytest
import unittest

from scraper import OdaScraper


class TestOdaScraper(unittest.TestCase):


    def test_price(self):
        decimal_point = OdaScraper.decimal_point
        currency = OdaScraper.currency

        with pytest.raises(RuntimeError):
            OdaScraper.parse_price(f"Dollars 100{decimal_point}67")

        with pytest.raises(RuntimeError):
            OdaScraper.parse_price(f"{currency} 100.67")

        with pytest.raises(RuntimeError):
            OdaScraper.parse_price(f"{currency} 100{decimal_point}x7")

        price, unit = OdaScraper.parse_price(f"{currency} 100{decimal_point}70 kr per kg")
        assert price == 100.70
        assert unit == "kr per kg"

        price, unit = OdaScraper.parse_price(f"{currency} 100{decimal_point}70")
        assert price == 100.70
        assert unit == ""


    def test_single_product_page(self):
        os = OdaScraper()
        fish_catalog = os.fetch_products("/no/categories/488-mathall/498-fiskedisken/")
        assert len(fish_catalog.products) == 41
        assert fish_catalog.products[0].name == "Levende Blåskjell"
        assert len(fish_catalog.categories) == 0
        assert fish_catalog.name == "Fiskedisken"


    def test_nested_product_page(self):
        os = OdaScraper()
        fruit_catalog = os.fetch_products("/no/categories/20-frukt-og-gront/21-fruit/")
        assert fruit_catalog.name == "Frukt"
        assert len(fruit_catalog.categories) == 7
        expected = [("Epler og pærer", 13),
                    ("Sitrusfrukter", 16),
                    ("Bananer", 4),
                    ("Meloner", 5),
                    ("Eksotiske frukter", 8),
                    ("Druer, kiwi og steinfrukt", 14),
                    ("Fruktkurv", 2)]

        for e,c in zip(expected, fruit_catalog.categories):
            assert e[0] == c.name
            assert e[1] == len(c.products)
