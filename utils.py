# -*- coding: utf-8 -*-
"""
Created on Sat May  4 19:32:13 2019

@author: Gabe Freedman
"""

import re

def yes_no_prompt(prompt):
    valid_answers = ['y', 'yes', 'n', 'no']
    
    while True:
        try:
            answer = input(prompt).lower()
        except ValueError:
            print('Invalid input type. Strings only, please.')
            continue

        if answer not in valid_answers:
            print('Invalid answer, must be y/n response.')
            continue
        else:
            break
    
    if answer in ['y', 'yes']:
        return True

def parse_tickers(symbol):
    pattern = r',\s+|\s+'

    symbol = symbol.upper()
    symbol = re.split(pattern, symbol)
    symbol = list(filter(None, symbol))

    return symbol

def parse_input(prompt):
    response = input(prompt).upper()
    
    if response == 'EXIT':
        return
    else:
        return response

def ask_question(prompt, validate, error, func):
    
    while True:
        response = input(prompt)
        if not validate(response):
            print(error)
            continue
        return response
