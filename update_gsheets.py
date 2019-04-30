# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 22:27:35 2019

@author: Gabe Freedman
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('finance-tracking-bd0390784e7a.json', scope)
client = gspread.authorize(credentials)

worksheet = client.open('Index Tracking').sheet1

cell_list = worksheet.range('C7:H14')

for i, cell in enumerate(cell_list):
    cell.value = 'Test_' + str(i+1)

worksheet.update_cells(cell_list)


start_row = 3
start_col = 'B'

def get_cell_range(df):
    
    cols = len(df.columns)
    rows = len(df)
    
    cell_range = '{}{}:{}{}'.format(start_col, start_row,
                                    cell_end_col(cols), cell_end_row(rows))
    return cell_range

def cell_end_row(rows):
    new_row = start_row + rows
    return new_row

def cell_end_col(cols):
    new_col = ''
    
    if (ord(start_col)+cols) > 90:
        new_col += 'A'
        cols = cols-26
    
    charnum = ord(start_col)+cols
    new_col += chr(charnum)
    
    return new_col
    
class CellRange:
    
    def __init__(self, start_col='B', start_row=3):
        self.start_col = start_col
        self.start_row = start_row
