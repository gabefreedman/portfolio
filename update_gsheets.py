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
