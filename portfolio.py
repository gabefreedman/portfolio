# -*- coding: utf-8 -*-

# Global imports
import pandas as pd
import fix_yahoo_finance as yf

from update_gsheets import Table


s_name = 'MSFT'
s = yf.Ticker(s_name)


# Dummy classes for Indices and Portfolios. Will fill in later

class Index:
    
    def __repr__(self):
        return 'Index object {}'.format(self.name)
    
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
        columns = ['shortName', 'marketCap',
                   'forwardPE', 'trailingPE',
                   'trailingAnnualDividendRate',
                   'regularMarketDayRange', 'fiftyTwoWeekRange',
                   'fiftyDayAverage', 'fiftyDayAverageChangePercent',
                   'twoHundredDayAverage', 'twoHundredDayAverageChangePercent']
        metadata = self.index_metadata()
        df = pd.DataFrame(metadata).T
        df = df[columns]
        df = df.set_index('shortName')
        return df

class Portfolio:
    pass

class WatchList(Index):
    # Will fill in later
    # Contains all tickers to watch on daily basis, regardless if they are currently owned.
    pass

def check_for_real_ticker(ind):
    empty_tickers = []
    for key, tick in ind.tick_items.items():
        if not tick.info:
            empty_tickers.append(key)

    for key in empty_tickers:
        ind.remove_company(key)
    if empty_tickers:
        print('The following tickers did not exist and were not added to the Index')
        print([item for item in empty_tickers])

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
    
    check_for_real_ticker(index)
    
    return index
