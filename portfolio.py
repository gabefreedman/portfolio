# -*- coding: utf-8 -*-

# Global imports
import pandas as pd
import fix_yahoo_finance as yf


s_name = 'MSFT'
s = yf.Ticker(s_name)


# Dummy classes for Indices and Portfolios. Will fill in later

class Index:
    def __init__(self, name):
        self.name = name
        self.tick_items = {}
    
    def add_company(self, ticker):
        s = yf.Ticker(ticker)
        self.tick_items[ticker] = s
    
    def remove_company(self, ticker):
        self.tick_items.pop(ticker)
    
    def index_metadata(self):
        metadata = {k: v.info for k, v in self.tick_items.items()}
        return metadata
    
    def main_metrics_table(self):
        columns = ['marketCap', 'forwardPE', 'trailingPE',
                   'trailingAnnualDividendRate',
                   'regularMarketDayRange', 'fiftyTwoWeekRange',
                   'fiftyDayAverage', 'fiftyDayAverageChangePercent',
                   'twoHundredDayAverage', 'twoHundredDayAverageChangePercent']
        metadata = self.index_metadata()
        df = pd.DataFrame(metadata).T
        df = df[columns]
        df.to_csv('daily_financial_metrics.csv')
        return df

class Portfolio:
    pass

class WatchList(Index):
    # Will fill in later
    # Contains all tickers to watch on daily basis, regardless if they are currently owned.
    pass

def build_index(name, companies=None):
    ''' Create custom Index object to store stock information
    
    Parameters
    ----------
    name (str) : Name for Index object (eg. VICE, ABCD, SMMR)
    companies (list, optional) : If provided, list of companies to add to index
                                 Calls add_company class function
    
    Returns
    -------
    index (Index) : Index object containing list of companies as Stock instances
    
    '''
    
    index = Index(name)
    
    if companies:
        # Force uppercase for ticker symbols
        # Remove duplicate tickers
        companies = [x.upper() for x in companies]
        companies = list(set(companies))
        for cmp in companies:
            index.add_company(cmp)
    
    return index
