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
# tabcustom.csv: custom tables created not included in table find analysis 
# make a list for each table in order to sent to sql query
# 10 parameter per group
# line will take table name
#
#
#

# +
def validatab(ruta, datb, ftab):
    import pandas as pd
    from pathlib import Path
    from datetime import date
    import sqlite3

    dat_dir = Path(ruta)
    tabex = 'tabcustom.csv' # tables to exclude 
    tex = pd.read_csv(dat_dir / tabex) 
    tlstex = list(tex.table_name)
    db_path1 = dat_dir / datb
    conn = sqlite3.connect(db_path1)  # database connection
    c = conn.cursor()
    ftab1 = ftab + '.csv' # parameters to get tables
    df1 = pd.read_csv(dat_dir / ftab1)
    try:
        df = pd.read_sql_query("select * from Fulltabcol;", conn) # tables related to parameter list
        common = df1.merge(df, on=["parameter"]) # paramerter table merge
        common = common[['table_name','parameter']] # change column order
        common = common[~common.table_name.isin(tlstex)] # common only with default tables
        grouped = common.groupby('table_name')
        grouped.first()
        
#         df.query('b == ["a", "b", "c"]')
#         df[df['b'].isin(["a", "b", "c"])]
        
        
        
#         output = 'tabparam.csv'
#         common.to_csv(dat_dir / output)
    except sqlite3.Error as error:  # sqlite error handling.
                        print('SQLite error: %s' % (' '.join(error.args)))
                        feedbk = tk.Label(top, text='SQLite error: %s' % (' '.join(error.args)))
                        feedbk.pack()
     
# -

validatab("C:/SQLite", "20200522_sqlite.db", "findtable")



# +
import pandas as pd
from pathlib import Path
from datetime import date
import sqlite3
df = pd.DataFrame({'time':[9,9,33,47,47,100,120,120],'block':[25,25,35,4,17,21,21,36],'cell': ['c1','c1','c2','c1','c2','c1','c1','c2']})

df

# +
grouped = df.groupby('time')

grouped.first(10)

# -

grouped.get_group(120) 

# +
final_df = pd.DataFrame({'time':[] ,'block':[],'cell':[]})

for ind, gr in grouped:

    final_df = final_df.append(gr.drop_duplicates("cell"))
# -

final_df


