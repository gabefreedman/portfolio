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

# cell_list = worksheet.range('C7:H14')
'''
for i, cell in enumerate(cell_list):
    cell.value = 'Test_' + str(i+2)

worksheet.update_cells(cell_list)
'''

def get_cell_range(rows, cols, start_row=3, start_col='C'):
    
    end_row = cell_end_row(rows, start_row)
    end_col = cell_end_col(cols, start_col)
    
    cell_range = '{}{}:{}{}'.format(start_col, start_row,
                                    end_col, end_row)
    return cell_range

def cell_end_row(rows, start_row=3):
    new_row = start_row + rows
    return new_row

def cell_end_col(cols, start_col='C'):
    new_col = ''
    
    if (ord(start_col)+cols) > 90:
        new_col += 'A'
        cols = cols-26
    
    charnum = ord(start_col)+cols
    new_col += chr(charnum)
    
    return new_col
    
class CellRange:
    
    def __init__(self, df, start_col='C', start_row=3):
        self.data_table = df
        self.num_cols = len(df.columns)-1
        self.num_rows = len(df)
        self.start_col = start_col
        self.header_row = start_row
        self.column_name_range = get_cell_range(0, self.num_cols, self.header_row, self.start_col)
        self.data_range = get_cell_range(self.num_rows-1, self.num_cols, self.header_row+1, self.start_col)
        
    def write_column_names(self):
        cell_list = worksheet.range(self.column_name_range)
        for i, cell in enumerate(cell_list):
            cell.value = self.data_table.columns[i]
        worksheet.update_cells(cell_list)
    
    def write_row_names(self):
        
    
    def write_data(self):
        cell_list = worksheet.range(self.data_range)
        flat_data = []
        
        for row in self.data_table.itertuples():
            flat_data.append(row[1:])
        
        full_data = []
        for item in flat_data:
            for i, j in enumerate(item):
                full_data.append(j)
        full_data = [str(x) for x in full_data]
        for i, cell in enumerate(cell_list):
            cell.value = full_data[i]
        worksheet.update_cells(cell_list)
    
    def write_full_table(self):
        self.write_column_names()
        self.write_data()


