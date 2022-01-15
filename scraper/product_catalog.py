from dataclasses import dataclass

@dataclass
class Product:
    name : str
    url : str
    label_price  : float
    unit_price : float
    unit : str


    def data(self):
        return {"label_price" : self.label_price,
                "url" : self.url,
                "unit_price" : self.unit_price,
                "unit" : self.unit,
                "name" : self.name}

    def dump(self, prefix):
        return f"{prefix}: {self.name}   {self.unit_price} {self.unit}      {self.url}\n"


class ProductCatalog:

    def __init__(self, name):
        self.name = name
        self.products = []
        self.categories = []

    def add_product(self, product):
        self.products.append(product)

    def add_category(self, category):
        self.categories.append(category)

    def data(self):
        return {"name" : self.name,
                "products" : [p.data() for p in self.products],
                "categories" : [c.data() for c in self.categories]}

    def dump(self, input_prefix=""):
        s = ""
        for prod in self.products:
            s += prod.dump(input_prefix)

        for category in self.categories:
            prefix = f"{input_prefix}/{category.name}"
            s += category.dump(prefix)

        return s
