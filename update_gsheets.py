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

def write_to_gsheets(cell_range, data):
    cell_list = worksheet.range(cell_range)
    for i, cell in enumerate(cell_list):
        cell.value = data[i]
    worksheet.update_cells(cell_list)

def get_cell_range(rows, cols, start_row=3, start_col='C'):
    
    end_row = cell_end_row(rows, start_row)
    end_col = cell_end_col(cols, start_col)
    
    cell_range = '{}{}:{}{}'.format(start_col, start_row,
                                    end_col, end_row)
    return cell_range

def cell_end_row(rows, start_row=3):
    new_row = start_row + rows
    return new_row - 1

def cell_end_col(cols, start_col='C'):
    new_col = ''
    
    if (ord(start_col)+cols) > 90:
        new_col += 'A'
        cols = cols-26
    
    charnum = ord(start_col) + cols - 1
    new_col += chr(charnum)
    
    return new_col
    
class Table:
    
    def __init__(self, df, start_row=3, start_col='C'):
        self.row_names = df.index
        self.col_names = df.columns
        self.flat_data = [str(item) for row in df.values.tolist() for item in row]
        self.start_row = start_row
        self.start_col = start_col
    
    def get_row_cells(self):
        num_rows = len(self.row_names)
        index_col = cell_end_col(0, self.start_col)
        
        cells = get_cell_range(num_rows, 1, self.start_row+1, index_col)
        return cells
    
    def get_col_cells(self):
        num_cols = len(self.col_names)
        
        cells = get_cell_range(1, num_cols, self.start_row, self.start_col)
        return cells
    
    def get_data_cells(self):
        num_rows = len(self.row_names)
        num_cols = len(self.col_names)
        
        cells = get_cell_range(num_rows, num_cols, self.start_row+1, self.start_col)
        return cells
    
    def write_table(self):
        
        write_to_gsheets(self.get_row_cells(), self.row_names)
        write_to_gsheets(self.get_col_cells(), self.col_names)
        write_to_gsheets(self.get_data_cells(), self.flat_data)
