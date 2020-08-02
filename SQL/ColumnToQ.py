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

import pandas as pd
import sqlite3
from pathlib import Path


# ctoq() save transposed table column names in csv file

def ctoq(ruta, datb, table):
    dat_dir = Path(ruta)
    db_path1 = dat_dir / datb
    conn = sqlite3.connect(db_path1)                # database connection
    c = conn.cursor()
    df = (pd.read_sql_query("SELECT name FROM pragma_table_info ('" + table + "');", conn).T)
    df = table + '.' + df
    csv_loc = table + '_head.csv'   # csv file name
    df.to_csv(dat_dir / csv_loc, header = False, index = False)       # pandas dataframe saved to csv
    c.close()
    conn.close()    


ctoq("C:/SQLite", "20200522_sqlite.db", 'WCEL')


