import re

from .product_catalog import ProductCatalog, Product
from .util import Fetcher


class OdaScraper:
    host = "https://oda.com"
    root = "/no/products/"
    currency = "kr"
    decimal_point = ","
    price_regexp = re.compile(fr"({currency})\s+(?P<amount>\d+){decimal_point}(?P<decimal_amount>\d+)(\s+(?P<unit>.+))?$")

    def __init__(self, max_bandwidth=0):
        self.fetcher = Fetcher(max_bandwidth=max_bandwidth)

    def url(self, path):
        return self.host + path


    def make_category(self, dom):
        category_name = dom.span.text.strip()
        return ProductCatalog(category_name)


    def make_sub_category(self, dom):
        category_name = dom.text.strip()
        return ProductCatalog(category_name)


    @classmethod
    def parse_price(cls, price_string):
        match_obj = cls.price_regexp.search(price_string)
        if match_obj is None:
            raise RuntimeError(f"Could not parse price string: '{price_string}'")

        price = float(match_obj.group("amount")) + float(match_obj.group("decimal_amount")) * 0.01
        unit = match_obj.group("unit")
        if unit is None:
            unit = ""
        return price,unit


    def make_product(self, dom):
        lp = dom.find("p", class_="label-price")
        label_price = 100
        try:
            label_price, _ = self.parse_price(lp.text.strip())
        except:
            pass

        up = dom.find("p", class_="unit-price")
        unit_price, unit = self.parse_price(up.text.strip())

        name_elm = dom.find("div", class_="name-main")
        name = name_elm.text.strip()
        url = dom["href"]

        return Product(name, url, unit_price, label_price, unit)


    def fetch_products(self, url):
        full_page = self.fetcher.fetch_dom(self.url(url))
        if not full_page:
            return None

        header_dom = full_page.dom.find("div", "product-category-header")
        header = header_dom.h3.text.strip()
        catalog = ProductCatalog(header)

        sub_categories = full_page.dom.find_all("h4", "child-category-headline")
        if sub_categories:
            for sub_cat in sub_categories:
                anchor = sub_cat.find("a", "headline")
                sub_catalog = self.fetch_products(anchor["href"])
                catalog.add_category(sub_catalog)

        else:
            products_dom = full_page.dom.find_all("a", "modal-link")
            for p in products_dom:
                catalog.add_product( self.make_product(p) )
        return catalog



    def run(self):
        catalog = ProductCatalog("Oda catalog")
        top_categories = self.fetcher.fetch_dom(self.url(self.root), class_filter = ("a", "product-category__link"))
        if top_categories:
            for cat in top_categories.dom:
                top_cat = self.make_category(cat)
                catalog.add_category(top_cat)
                sub_categories = self.fetcher.fetch_dom(self.url(cat["href"]), class_filter = ("a", "headline"))

                if sub_categories:
                    for sub_cat in sub_categories.dom:
                        sub_catalog = self.make_sub_category(sub_cat)
                        top_cat.add_category(sub_catalog)

                        products = self.fetch_products(sub_cat["href"])
                        sub_catalog.add_category(products)

        return catalog
