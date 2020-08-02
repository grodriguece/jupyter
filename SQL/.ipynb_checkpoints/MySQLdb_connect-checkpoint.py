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

import os
import MySQLdb as mdb

# +
DBNAME = "dbtest"
DBHOST = "localhost"
DBUSER = os.environ.get('DB_USER')
DBPASS = os.environ.get('DB_PASS')

try:
    db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)
    print('database connect ok')

except mdb.Error as e:
    print("database not connected")
    
# -

jupytext --to py MySQLdb_connect.ipynb

jupytext --to py MySQLdb_connect.ipynb


