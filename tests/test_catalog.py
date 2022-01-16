import datetime
import unittest
import pytest

from scraper.product_catalog import *

class TestProductCatalog(unittest.TestCase):


    def test_catalog(self):
        catalog = ProductCatalog("Drikke")
        grans_beer = Product(1, "Grans pils", "url", 100, 50, "l")
        catalog.add_product(grans_beer)

        soda = ProductCatalog("Brus")
        cola = Product(4, "Cola", "url", 1, 2, "l")
        solo = Product(5, "Solo", "url", 3, 4, "l")
        soda.add_product(cola)
        soda.add_product(solo)


        milk = ProductCatalog("Melk")
        whole_milk = Product(2, "H-melk", "url", 7, 8, "l")
        skimmed_milk = Product(3, "Skummet melk", "url", 5, 6, "l")
        milk.add_product(whole_milk)
        milk.add_product(skimmed_milk)

        catalog.add_category(milk)
        catalog.add_category(soda)

        data = catalog.data()

        expected = {
            "name": "Drikke",
            "products": [
                {
                    "id" : 1,
                    "url" :"url",
                    "name": "Grans pils",
                    "label_price": 100,
                    "unit_price": 50,
                    "unit": "l"
                }
            ],
            "categories": [
                {
                    "name": "Melk",
                    "categories": [],
                    "products": [
                        {
                            "id" : 2,
                            "url" :"url",
                            "name": "H-melk",
                            "label_price": 7,
                            "unit_price": 8,
                            "unit": "l"
                        },
                        {
                            "id" : 3,
                            "url" :"url",
                            "name": "Skummet melk",
                            "label_price": 5,
                            "unit_price": 6,
                            "unit": "l"
                        }
                    ]
                },
                {
                    "name": "Brus",
                    "categories": [],
                    "products": [
                        {
                            "id" : 4,
                            "url" :"url",
                            "name": "Cola",
                            "label_price": 1,
                            "unit_price": 2,
                            "unit": "l"
                        },
                        {
                            "id" : 5,
                            "url" :"url",
                            "name": "Solo",
                            "label_price": 3,
                            "unit_price": 4,
                            "unit": "l"
                        }
                    ]
                }
            ]
        }

        assert data == expected
