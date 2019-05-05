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