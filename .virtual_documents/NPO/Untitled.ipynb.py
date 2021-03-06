# import numpy as np
from plotnine import *
import pandas as pd
import openpyxl
import csv
# from xlsx2csv import Xlsx2csv
from rfpack.get_sheet_detailsc import get_sheet_details
from xlsx2csv import *
from pathlib import Path
import sys, os, json, re, time
import subprocess
from pathlib import Path
import os
import xmltodict
import shutil
import zipfile


# def get_sheet_details(filename):
#     sheets = []
#     # Make a temporary directory with the file name
#     # directory_to_extract_to = Path(ruta + filename)
#     directory_to_extract_to = (filename.with_suffix(''))
#     os.mkdir(directory_to_extract_to)
#     # Extract the xlsx file as it is just a zip file
#     # zip_ref = zipfile.ZipFile(Path(ruta + filename + '.xlsx'), 'r')
#     zip_ref = zipfile.ZipFile(filename, 'r')
#     zip_ref.extractall(directory_to_extract_to)
#     zip_ref.close()
#     # Open the workbook.xml which is very light and only has meta data, get sheets from it
#     path_to_workbook = directory_to_extract_to / 'xl' / 'workbook.xml'
#     with open(path_to_workbook, 'r') as f:
#         xml = f.read()
#         dictionary = xmltodict.parse(xml)
#         for sheet in dictionary['workbook']['sheets']['sheet']:
#             sheet_details = {
#                 'id': sheet['@sheetId'],  # can be sheetId for some versions
#                 'name': sheet['@name']  # can be name
#             }
#             sheets.append(sheet_details)
#     # Delete the extracted files directory
#     shutil.rmtree(directory_to_extract_to)
#     return sheets  # with sheetid, it can be saved with xlsx2csv


def get_key(val):
    for key, value in my_dict.items(): 
         if val == value: 
             return key 
    return "key doesn't exist"


def get_sheetid_bynamei(item, dict):
    import pandas as pd
    df2 = pd.DataFrame.from_dict(dict)
    df1 = df2[(df2['name'] == item)].reset_index()
    return df1


def get_sheetid_bynamef(tablas, tipo, dict):
    import pandas as pd
    df2 = pd.DataFrame.from_dict(dict)
    df1 = pd.read_csv(tablas)
    df1 = df1.loc[:, df1.columns == tipo].dropna()  # only column tipo is selected without NaN
    df1.rename(columns={tipo: "name"}, inplace=True)
    df1 = pd.merge(df1, df2, on='name')
    return df1


def csvfrmxlsx(xlsxfl, df):  # create csv files in csv folder on parent directory
    from pathlib import Path
    from xlsx2csv import Xlsx2csv
    for index, row in df.iterrows():  # table row iteration by audit2 column type
        shnum = row['id']
        shnph = xlsxfl.parent / 'csv' / Path(row['name'] + '.csv')  # path for converted csv file
        Xlsx2csv(str(xlsxfl), outputencoding="utf-8").convert(str(shnph), sheetid=int(shnum))  # id from openxlsx
    return


def graffull(ruta, df):
    print
    dat_dir = Path(ruta)
    xls_file = fname + ".xlsx"
    xls_path = dat_dir / xls_file





rffl = 'tablasSQL.csv'
clmntp = 'xlsxsheets'
pthfnc = 'c:/sqlite/'
wrkfl = '200820_Feat1ParAudit.xlsx'
xls_file = Path(pthfnc + wrkfl)
rfflph = Path(pthfnc + rffl)
print(xls_file.stem)
print(xls_file.name)
print(xls_file.parent)
print(xls_file.suffixes)

sheetsdic = get_sheet_details(xls_file)  # get sheet names and ids without opening xlsx file
df = get_sheetid_bynamef(rfflph, clmntp, sheetsdic)  # xlsxsheets column from csv table file
# df = get_sheetid_bynamei("Total", sheetsdic)  # get sheet id from Total sheet
csvfrmxlsx(xls_file, df)  # df with sheets to be converted
graffull(xls_file.parent, df)



