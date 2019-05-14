# -*- coding: utf-8 -*-
"""
Created on Sat May  4 19:06:35 2019

@author: Gabe Freedman
"""

import sys
import pickle

from portfolio import build_index, check_for_real_ticker
from utils import yes_no_prompt, parse_tickers, parse_input

help_func = {'build' : 'Build Index from input ticker symbols',
            'exist' : 'Prints existing Index objects being tracked',
            'table' : 'Pick existing Index and update table of financial metrics',
            'edit' : 'Edit Index object, add or remove tickers',
            'exit' : 'Exit program',
            'remove' : 'Delete Index object',
            'save' : 'Save currently cached indices to file',
            'help' : 'Display available commands'}

CACHED_INDICES = []
CACHED_IND_NAMES = []

def _build():
    tick_items = []
    print('\n----------BUILD INDEX----------\n')
    change = 'n'
    while change in ['n', 'no']:
        ind_name = input('Enter a name for your index: ').upper()
        if ind_name in CACHED_IND_NAMES:
            dupl_ind = CACHED_IND_NAMES.index(ind_name)
            print('Index {} already exists.'.format(ind_name))
            print('Enter a different name or type \'replace\' to replace Index')
            replace_or_change = input('>>> ').lower()
            if replace_or_change == 'replace':
                CACHED_INDICES.pop(dupl_ind)
                CACHED_IND_NAMES.remove(ind_name)
            else:
                ind_name = replace_or_change.upper()
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
    CACHED_IND_NAMES.append(ind_name)
    print('Index {} created.'.format(ind_name))

def _exist():
    print('The following indices have already been created')
    print(CACHED_INDICES)

def _edit():
    print('Pick which Index to edit.')
    print(CACHED_IND_NAMES)
    edit_index = input('>>> ').upper()
    while edit_index not in CACHED_IND_NAMES:
        print('Cannot edit Index {}. Does not exist'.format(edit_index))
        print('Available indices: {}'.format(CACHED_IND_NAMES))
        print('Enter name of Index or type \'exit\' to return to main prompt.')
        edit_index = input('>>> ').upper()
        if edit_index == 'EXIT':
            return
    
    temp = CACHED_IND_NAMES.index(edit_index)
    ind = CACHED_INDICES[temp]
    print('Index name: {}'.format(ind.name))
    print('Tickers: {}'.format(list(ind.tick_items.keys())))
    print('Enter \'add\' or \'remove\' to edit ticker list')
    print('Enter \'exit\' to return to main prompt.')
    command = input('>>> ').lower()
    while command not in ['add', 'remove', 'exit']:
        print('Invalid command. Valid commands are \'add\', \'remove\', \'exit\'.')
        command = input('>>> ').lower()
    while command != 'exit':
        if command == 'add':
            add = input('Enter tickers to add: ')
            add = parse_tickers(add)
            for tck in add:
                ind.add_company(tck)
                check_for_real_ticker(ind)
            print('Index name: {}'.format(ind.name))
            print('Tickers: {}'.format(list(ind.tick_items.keys())))
        elif command == 'remove':
            remove = input('Enter tickers to remove: ')
            remove = parse_tickers(remove)
            for tck in remove:
                if tck in list(ind.tick_items.keys()):
                    ind.remove_company(tck)
            print('Index name: {}'.format(ind.name))
            print('Tickers: {}'.format(list(ind.tick_items.keys())))
        else:
            print('Invalid command. Valid commands are \'add\', \'remove\', \'exit\'.')
        command = input('>>> ')

def _table():
    ''' Test docstring again
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
    for key, val in help_func.items():
        print('{} : {}\n'.format(key, val))

def _load_pickle():
    with open('cached_indices.pickle', 'rb') as f:
        dat = pickle.load(f)
    CACHED_INDICES.extend(dat)
    CACHED_IND_NAMES.extend(ind.name for ind in CACHED_INDICES)

def _remove():
    ''' Test docstring
    Will provide additional commands here
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
            print('Index {} has been removed. Current indices are {}.'.format(response, CACHED_IND_NAMES))

def _save():
    with open('cached_indices.pickle', 'wb') as f:
        pickle.dump(CACHED_INDICES, f)

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
