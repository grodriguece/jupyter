# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Find Table for Parameter List
# tabcustom.csv: custom tables created not included in table find analysis<br> 
# make a list for each table in order to sent to sql query<br>
# 10 parameter per group<br>
# line will take table name

from datetime import date
from pathlib import Path
from pyexcelerate import Workbook
from pyexcelerate_to_excel import pyexcelerate_to_excel
from rfpack.validatabc import validatab
from rfpack.customparamc import customparam
from rfpack.pntopdc import pntopd
from rfpack.get_sheet_detailsc import get_sheet_details
from rfpack.get_sheetid_bynamec import *
from rfpack.csvfrmxlsxc import csvfrmxlsx
from rfpack.graffullc import graffull
from rfpack.xlsxreordc import xlsxreord
from rfpack.csvfrmxlsxc import xlsxfmcsv

datab = Path('C:/SQLite/20200522_sqlite.db')
pdf_file = date.today().strftime("%y%m%d") + '_Feat1ParAudit.pdf'
pdf_path = datab.parent / pdf_file
xls_file = Path(pdf_path.with_suffix('.xlsx'))
wb = Workbook()  # pyexcelerate Workbook
validatab(datab, 'findtable', 'tabcustom')  # locate input tab/parameters in dbabase
pnglist, sheetsdic = customparam(datab, 'tab_par')  # generates png files and create xlsx file
# rffl = 'C:/SQLite/tablasSQL.csv'  # sheets to select in xlsxsheets column
# rfflph = Path(rffl)
# clmntp = 'xlsxsheets'  # column to process in this case Total
# sheetsdic = get_sheet_details(xls_file)  # get sheet names and ids without opening xlsx file
# df = get_sheetid_bynamef(rfflph, clmntp, sheetsdic)  # xlsxsheets column from csv table file
# csvfrmxlsx(xls_file, df)  # df with sheets to be converted
pnglist1 = graffull(xls_file, 'Total', 4)  # print Total info in 4 pages, 3 regions per page
pnglist1.extend(pnglist) # review png at the beggining
pntopd(pdf_path, pnglist1, 50, 550, 500, 500)  # png to pdf
xlsxfmcsv(xls_file, sheetsdic)
# xlsxreord(xls_file, df.at[0, 'name'], 0)  # put review sheet at the beginning of the file

