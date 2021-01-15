
"""
Name: Category To Excel
Created: 12 Dec 2020[Version1],  14 Jan 2021[Version4]
Purpose: To Extract Category and Websites List and Create a Excel Sheet for easy view and access of SafeSquid Web Category
Script Requirement: 
=> Python3 v3.5+
=> Python Packages
    :- Pandas
    :- openpyxl

Tech End:
============

Short Explanation:
-----------------------

1) SafeSquid Stores Category as
   Website Name| All Category It Falls In

2) Data Received From SQLite DB Looks:
   Each Row is received as Tuple and can be Iterated

   ('amazon.com', ',Amazon SIte,')
   ('hdfcbank.com', ',banking,Company Banking Websites,')
   ('dst.com.ng', ',business,Company Blacklisted Websites,Job Search,Storage,')
   ('checkmarx.com', ',business,Company Blacklisted Websites,')
   ('microsoft.com', ',business,COMPANY ALLOWED WEBSITES,')

3) We then Split the Category and create a Unique Set For WebCategory and Any Website which has this in the List is added to that Web Category
Note: We Split it using "," and DO Not Process Any Empty Data

"""

import sqlite3
import json
import pandas as pd
from pandas import ExcelWriter

""" Get Data from The Category SQLite DB """
def get_category_database_set():
    #CATEGORY_DB_PATH = './test_files/category.db'; # Testing using Client Server
    CATEGORY_DB_PATH = '/var/lib/safesquid/category/category.db'
    CATEGORY_DB_SQL_QUERY = 'SELECT * from PRIVATE_CATEGORY;'
    sqlite3_db_connection = sqlite3.connect(CATEGORY_DB_PATH)
    db_cursor = sqlite3_db_connection.cursor()
    category_db_result_set = db_cursor.execute(CATEGORY_DB_SQL_QUERY);
    #sqlite3_db_connection.close() # Close the DB Connection [Creates Problem Therefore Omitted]
    return category_db_result_set

""" Start Building the Category JSON """
def build_category_data(category_db_result_set):
    category_list = {}
    category_list_json = []
    for one_row in category_db_result_set:
        website_name = one_row[0];
        website_category_list = one_row[1];
        for one_category_name in website_category_list.split(','):
            if one_category_name != '':
                if one_category_name in category_list.keys():
                    category_list.get(one_category_name).append(website_name); # Append to Website List of Category Already Identified & Added in JSON (Object)
                else:
                    category_list[one_category_name] = [website_name] # Create New WebCategory & Add New Website in the Website List in JSON (Object)
    return category_list

""" Generate Excel Sheet using OpenPyXL """
def generate_excel(category_list, category_sheet):
    _startcol = 0

    writer = pd.ExcelWriter(category_sheet, engine='openpyxl')

    for category_name, category_website_list in category_list.items():
        df = pd.DataFrame({ category_name: category_website_list } )
        df.to_excel(writer, startcol = _startcol, index=False, sheet_name='Web Category List')
        _startcol = _startcol + 1;

    writer.save()

""" Start The Processing """
def main():
    category_sheet = 'SafeSquid_Category_Sheet.xlsx'
    category_db_result_set = get_category_database_set()
    category_list = build_category_data(category_db_result_set)
    generate_excel(category_list=category_list, category_sheet=category_sheet)
    

main()