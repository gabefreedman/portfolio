# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:45:39 2019

@author: C009897
"""

import re
import sys
import pickle
import os

from portfolio import build_index

help_func = {'build' : 'Build Index from input ticker symbols',
            'exist' : 'Prints existing Index objects being tracked',
            'table' : 'Pick existing Index and update table of financial metrics',
            'exit' : 'Exit program', 
            'help' : 'Display available commands'}

CACHED_INDICES = []

def yes_no_prompt(prompt):
    valid_answers = ['y', 'yes', 'n', 'no']
    
    while True:
        try:
            answer = input(prompt)
        except ValueError:
            print('Invalid input type. Strings only, please.')
            continue

        if answer.lower() not in valid_answers:
            print('Invalid answer, must be y/n response.\n')
            continue
        else:
            break
    return answer.lower()

def parse_tickers(symbol):
    pattern = r',\s+|\s+'

    symbol = symbol.upper()
    symbol = re.split(pattern, symbol)
    symbol = list(filter(None, symbol))

    return symbol


def _build():
    tick_items = []
    print('\n----------BUILD INDEX----------\n')
    change = 'n'
    while change in ['n', 'no']:
        ind_name = input('Enter a name for your index: ').upper()
        if ind_name in [index.name for index in CACHED_INDICES]:
            dupl_ind = [index.name for index in CACHED_INDICES].index(ind_name)
            print('Index {} already exists.'.format(ind_name))
            print('Enter a different name or type \'replace\' to replace Index')
            replace_or_change = input('>>> ').lower()
            if replace_or_change == 'replace':
                CACHED_INDICES.pop(dupl_ind)
            else:
                ind_name = replace_or_change
        change = yes_no_prompt('Index name: {}. Is this correct? '.format(ind_name))
                

    print('Enter ticker symbols to add to index')
    tickers = input('>>> ')
    tickers = parse_tickers(tickers)
    tick_items.extend(tickers)
    print('Current tickers in {}: {}'.format(ind_name, tick_items))
    add_more = yes_no_prompt('Add more tickers to {}? '.format(ind_name))

    while add_more in ['y', 'yes']:
        print('Enter ticker symbols to add to index')
        tickers = input('>>> ')
        tickers = parse_tickers(tickers)
        tick_items.extend(tickers)
        print('Current tickers in {}: {}'.format(ind_name, tick_items))
        add_more = yes_no_prompt('Add more tickers to {}? '.format(ind_name))

    tick_items = list(set(tick_items))
    print('\nFinal index {}'.format(ind_name))
    print('Tickers: {}'.format(tick_items))
    print('To remove tickers type remove. Otherwise hit ENTER to build Index.')
    remove_or_build = input('>>> ')
    while remove_or_build == 'remove':
        remove_more = 'y'
        while remove_more in ['y', 'yes']:
            remove_tick = input('Which tickers would you like to remove? ')
            remove_tick = parse_tickers(remove_tick)
            tick_items = [x for x in tick_items if x not in remove_tick]
            print('Tickers: {}'.format(tick_items))
            remove_more = yes_no_prompt('Remove more tickers? ')

        print('\nFinal index {}'.format(ind_name))
        print('Tickers: {}'.format(tick_items))
        print('To remove tickers type remove. Otherwise hit ENTER to build Index.')
        remove_or_build = input('>>> ')

    ind = build_index(ind_name, tick_items)
    CACHED_INDICES.append(ind)
    print('Index {} created.'.format(ind_name))

def _exist():
    print('The following indices have already been created')
    print(CACHED_INDICES)

def _table():
    print('What table?')

def _help():
    print('--------AVAILABLE COMMANDS--------')
    for key, val in help_func.items():
        print('{} : {}\n'.format(key, val))

def _load_pickle():
    with open('cached_indices.pickle', 'rb') as f:
        dat = pickle.load(f)
    CACHED_INDICES.extend(dat)

def _save():
    with open('cached_indices.pickle', 'wb') as f:
        pickle.dump(CACHED_INDICES, f)

def _exit():
    _save()
    sys.exit(0)

commands = {'build' : _build,
            'exist' : _exist,
            'table' : _table,
            'exit' : _exit,
            'save' : _save,
            'help' : _help}

def main():
    print('\n---------STOCK INDEX CREATION AND TRACKING PROGRAM---------\n')
    print('Type \'help\' to show available commands')
    
    if os.path.isfile('cached_indices.pickle'):
        _load_pickle()
    
    input1 = input('>>> ')
    while input1 != 'exit':
        while input1 not in commands.keys():
            print('Invalid command. Type \'help\' for available commands')
            input1 = input('>>> ')

        commands[input1]()
        
        input1 = input('>>> ')
    
    _exit()

if __name__ == '__main__':
    main()

