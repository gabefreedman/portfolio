# -*- coding: utf-8 -*-

# Global imports
import pandas as pd

# Then relative imports
from wallstreet import Stock


s_name = 'MSFT'
s = Stock(s_name)


# Dummy classes for Indices and Portfolios. Will fill in later

class Index:
    def __init__(self, name):
        self.name = name

class Portfolio:
    pass

