# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:45:39 2019

@author: C009897
"""

import re

commands = ['build', 'exist']

valid_answers = ['y', 'yes', 'n', 'no']

def yes_no_prompt(prompt):
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

def build_index():
    print('Index has been built. Yay.')
    

def _build():
    tick_items = []
    print('\n----------BUILD INDEX----------\n')
    change = 'n'
    while change in ['n', 'no']:
        ind_name = input('Enter a name for your index: ').upper()
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
    
    build_index()
    print('We\'re done here.')
    

print('---------STOCK INDEX CREATION AND TRACKING PROGRAM---------')
print('\n\nAvailable commands:')
print('\tbuild : Build Index from input ticker symbols')
print('\texist : Prints existing Index objects being tracked')

input1 = input('>>> ')
while input1 not in commands:
    print('Invalid command. Available commands are [' + ', '.join(commands) + ']')
    input1 = input('>>> ')

print('You entered: {}'.format(input1))

if input1 == 'build':
    _build()
