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

# HeidiSQL, MySQL client
# https://pypi.org/project/mysql-connector-python/

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sb
# %matplotlib inline

user_name = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS')

# +
mydb=mysql.connector.connect(host='localhost', user=user_name, passwd=password, 
                             auth_plugin = 'mysql_native_password', db='employees')
mydb
# c=mydb.cursor()
# c.execute("Show databases")
# for db in c:
#     print(db)

# conn = sqlite3.connect('sakila-db/sakila.db')
# -

# use=pd.read_sql_query('USE employees',mydb)
employees_tables = pd.read_sql_query('show tables from employees',mydb)

employees_tables

tables = employees_tables['Tables_in_employees']

for table_name in tables:
    output = pd.read_sql_query('DESCRIBE ' + table_name, mydb)
    print(table_name)
    print(output, '\n')

employees_hired_year = 'SELECT YEAR(e.hire_date) as hire_date, COUNT(e.emp_no) as employee_count\
                        FROM employees e\
                        GROUP BY YEAR(e.hire_date)\
                        ORDER BY hire_date asc'

df = pd.read_sql_query(employees_hired_year,mydb)

df

employees_table = 'SELECT * FROM employees'

df = pd.read_sql_query(employees_table,mydb)

df

df['hire_year']=df['hire_date'].apply(lambda date:date.year)

df

df.groupby(['hire_year'])['emp_no'].count()

print("hello world")
print("hello world")
print("hello world")
print("hello world")
