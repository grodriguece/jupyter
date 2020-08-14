def tabconv(tabsent):
    switcher = {
        'LNCEL': 'LNCEL_Full',
        'LNHOIF': 'LNHOIF_ref',
        'LNBTS': 'LNBTS_Full',
        'LNHOW': 'LNHOW_ref',
        'WCEL': 'WCEL_FULL1',
        'RNFC': 'RNFC_ref',
        'AMLEPR': 'AMLEPR_ref',
        'ANRPRL': 'ANRPRL_ref',
        'LNREL': 'LNREL_NO',
        'IRFIM': 'IRFIM_ref',
        'UFFIM_UTRFDDCARFRQL': 'UFFIM_UTRFDDCARFRQL_ref',
        'IAFIM_INTRFRNCLIST': 'IAFIM_INTRFRNCLIST_ref',
        'UFFIM': 'UFFIM_ref',
    }
    return switcher.get(tabsent, 'nothing') # 'nothing' if not found


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
        common = common[['table_name', 'parameter']] # change column order
        common = common[~common.table_name.isin(tlstex)] # common only with default tables
        output = 'tabparam.csv'
        common.to_csv(dat_dir / output)
        common1 = common.groupby('table_name')['parameter'].apply(list).reset_index(name='parlist')
        print(common1)
        for index, row in common1.iterrows():
            print(row['table_name'], row['parlist']) # include prefijo and uarfcn in sql orig query
            params = row['parlist']
            params.append('Prefijo', 'LNBTS_id')
            partosql = tuple(params, row['table_name'])
            
            tabsq = tabconv(row['table_name'])
            # parsrch = tuple(row['parlist'])

#             q = """
#              select get_ipython().run_line_magic("s", "")
#              from get_ipython().run_line_magic("s", " ")
#              ;
#              """
            
            
                dft = pd.read_sql_query("select ? from ?;", conn, params=(region, feature , newUser))  # ,index_col='WCELName')
            dft = dft[['Prefijo'], row['parlist']]
            print(dft)


    # parsrch = (111, 222, 333, 444, 555)  # requires to be a tuple

    # query = f"""
    #     SELECT par_id FROM""" +  tabsq +
    #     """WHERE par_id IN {parsrch}
    # """

    # df = pd.read_sql_query(query, db2conn)


#         df.query('b == ["a", "b", "c"]')
#         df[df['b'].isin(["a", "b", "c"])]
        
        
        
#         output = 'tabparam.csv'
#         common.to_csv(dat_dir / output)
    except sqlite3.Error as error:  # sqlite error handling.
                        print('SQLite error: get_ipython().run_line_magic("s'", " % (' '.join(error.args)))")
                        feedbk = tk.Label(top, text='SQLite error: get_ipython().run_line_magic("s'", " % (' '.join(error.args)))")
                        feedbk.pack()
     


validatab("C:/SQLite", "20200522_sqlite.db", "findtable")
