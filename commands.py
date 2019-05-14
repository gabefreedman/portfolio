# -*- coding: utf-8 -*-
"""
Created on Sat May  4 19:06:35 2019

@author: Gabe Freedman
"""

import sys
import pickle
import re

from portfolio import build_index, check_for_real_ticker
from utils import yes_no_prompt, parse_tickers, parse_input

HELP_FUNC = {'build' : 'Build Index from input ticker symbols',
             'exist' : 'Prints existing Index objects being tracked',
             'table' : 'Pick existing Index and update table of financial metrics',
             'edit' : 'Edit existing Index object, add or remove tickers',
             'exit' : 'Exit program',
             'remove' : 'Delete Index object',
             'save' : 'Save currently cached indices to file',
             'help' : 'Display available commands'}

CACHED_INDICES = []
CACHED_IND_NAMES = []

def _add_tickers(ind):
    ''' Add ticker(s) to Index.
    Valid characters are a-z, A-Z, whitespace and commas.
    '''
    pattern = re.compile('^[a-zA-Z, ]+$')
    print('Enter tickers to add.')
    response = parse_input('>>> ', pattern.match,
                           'Invalid characters entered.', _add_tickers)
    if response:
        response = parse_tickers(response)
        for ticker in response:
            ind.add_company(ticker)
            check_for_real_ticker(ind)
        print('Index name: {}'.format(ind.name))
        print('Tickers: {}'.format(list(ind.tick_items.keys())))

def _remove_tickers(ind):
    ''' Remove ticker(s) from Index.
    Valid characters are a-z, A-Z, whitespace and commas.
    '''
    pattern = re.compile('^[a-zA-Z, ]+$')
    print('Enter tickers to remove.')
    response = parse_input('>>> ', pattern.match,
                           'Invalid characters entered.', _remove_tickers)
    if response:
        response = parse_tickers(response)
        for ticker in response:
            if ticker in list(ind.tick_items.keys()):
                ind.remove_company(ticker)
        print('Index name: {}'.format(ind.name))
        print('Tickers: {}'.format(list(ind.tick_items.keys())))

def _build():
    ''' Build new Index object
    Step 1: Index name. Valid characters are a-z, A-Z, whitespace and commas.
    Step 2: Ticker list. Valid commands are \'add\' and \'remove\'
    '''
    print('Enter a name for your index.')
    response = parse_input('>>> ', lambda s: s not in CACHED_IND_NAMES,
                           'Index already exists.', _build)
    if response:
        ind = build_index(response)
        CACHED_INDICES.append(ind)
        CACHED_IND_NAMES.append(response)
        print('Enter \'add\' or \'remove\' to edit tickers')

        action = True
        while action:
            action = parse_input('>>> ', lambda s: s in ['ADD', 'REMOVE'],
                                 'Invalid command.', _build)
            if action == 'ADD':
                _add_tickers(ind)
            elif action == 'REMOVE':
                _remove_tickers(ind)

def _exist():
    print('The following indices have already been created')
    print(CACHED_INDICES)

def _edit():
    ''' Edit existing Index object
    Step 1: Index name. Valid characters are a-z, A-Z, whitespace and commas.
    Step 2: Ticker list. Valid commands are \'add\' and \'remove\'
    '''
    print('Choose Index to edit.')
    print('Available indices: {}'.format(CACHED_IND_NAMES))
    response = parse_input('>>> ', lambda s: s in CACHED_IND_NAMES,
                           'Index does not exist', _edit)

    if response:
        idx = CACHED_IND_NAMES.index(response)
        ind = CACHED_INDICES[idx]
        print('Index name: {}'.format(ind.name))
        print('Tickers: {}'.format(list(ind.tick_items.keys())))
        print('Enter \'add\' or \'remove\' to edit ticker list')

        action = True
        while action:
            action = parse_input('>>> ', lambda s: s in ['ADD', 'REMOVE'],
                                 'Invalid command.', _edit)
            if action == 'ADD':
                _add_tickers(ind)
            elif action == 'REMOVE':
                _remove_tickers(ind)

def _table():
    ''' Update table of financial metrics for given Index
    Valid commands: \'all\', (Index name)
    '''
    print('Type the name of the Index to create / update table.')
    print('Available indices: {}'.format(CACHED_IND_NAMES))
    response = parse_input('>>> ',
                           lambda s: (s in CACHED_IND_NAMES) or (s == 'ALL'),
                           'Index does not exist.', _table)

    if response == 'ALL':
        for ind in CACHED_INDICES:
            ind.save_table()
        print('Tables successfully updated.')
    elif response:
        idx = CACHED_IND_NAMES.index(response)
        CACHED_INDICES[idx].save_table()
        print('Table successfully updated.')

def _help():
    print('-----------AVAILABLE COMMANDS-----------\n')
    for key, val in HELP_FUNC.items():
        print('{} : {}\n'.format(key, val))

def _load_pickle():
    with open('cached_indices.pickle', 'rb') as file:
        data = pickle.load(file)
    CACHED_INDICES.extend(data)
    CACHED_IND_NAMES.extend(ind.name for ind in CACHED_INDICES)

def _remove():
    ''' Delete Index object
    Valid input: name of Index
    '''
    print('Type the name of the Index you\'d like to remove.')
    print('Current indices are {}.'.format(CACHED_IND_NAMES))
    response = parse_input('>>> ', lambda s: s in CACHED_IND_NAMES,
                           'Index does not exist.', _remove)

    if response:
        print('Are you sure you want to delete {}?'.format(response))
        confirm = yes_no_prompt('>>> ')
        if confirm:
            remove_index = CACHED_IND_NAMES.index(response)
            CACHED_INDICES.pop(remove_index)
            CACHED_IND_NAMES.remove(response)
            print('Index {} has been removed.'.format(response))
            print('Current indices are {}.'.format(CACHED_IND_NAMES))

def _save():
    with open('cached_indices.pickle', 'wb') as file:
        pickle.dump(CACHED_INDICES, file)

def _exit():
    _save()
    sys.exit(0)

command_prompts = {'build' : _build,
                   'exist' : _exist,
                   'table' : _table,
                   'edit' : _edit,
                   'exit' : _exit,
                   'remove' : _remove,
                   'save' : _save,
                   'help' : _help}
