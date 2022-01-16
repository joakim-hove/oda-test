import datetime
import pytest
import unittest

from scraper import OdaScraper, Product


class TestOdaScraper(unittest.TestCase):

    oda_host = "https://oda.com"



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
        os = OdaScraper(self.oda_host)
        fish_catalog = os.fetch_products("/no/categories/488-mathall/498-fiskedisken/")
        assert len(fish_catalog.products) == 41
        assert fish_catalog.products[0].name == "Levende Blåskjell"
        assert len(fish_catalog.categories) == 0
        assert fish_catalog.name == "Fiskedisken"


    def test_nested_product_page(self):
        os = OdaScraper(self.oda_host)
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


        expected_apples = [ Product(26541,
                                    "Pink Lady Epler",
                                    "/no/products/26541-pink-lady-epler-italia/",
                                    39.90,
                                    46.94,
                                    "per kg"),
                            Product(27169,
                                    "Epler, Grønne, 6 pk",
                                    "/no/products/27169-epler-gronne-6-pk-granny-smith-italia/",
                                    25.60,
                                    28.44,
                                    "per kg")]


        apples = fruit_catalog.categories[0].products
        for test_index in range(len(expected_apples)):
            assert expected_apples[test_index] == apples[test_index]
