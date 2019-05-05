# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:45:39 2019

@author: C009897
"""

import os

import commands as cmd

def main():
    print('\n---------STOCK INDEX CREATION AND TRACKING PROGRAM---------\n')
    print('Type \'help\' to show available commands')
    
    if os.path.isfile('cached_indices.pickle'):
        cmd._load_pickle()
    
    input1 = input('>>> ')
    while input1 != 'exit':
        while input1 not in cmd.command_prompts.keys():
            print('Invalid command. Type \'help\' for available commands')
            input1 = input('>>> ')

        cmd.command_prompts[input1]()
        
        input1 = input('>>> ')
    
    cmd._exit()

if __name__ == '__main__':
    main()

