# -*- coding: utf-8 -*-
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

# # Parameter - Audit LNBTS


#  [boxplot](http://www.math.wpi.edu/saspdf/stat/chap18.pdf)
#  [git](http://wresch.github.io/2013/03/08/asinh-scales-in-ggplot2.html)
#  [stack](https://stackoverflow.com/questions/37446064/i-need-ggplot-scale-x-log10-to-give-me-both-negative-and-positive-numbers-as-o)
#  
# [import](https://www.tutorialspoint.com/python/python_modules.htm)
#
# [PATH](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages)
#
# [stats](https://ademos.people.uic.edu/Chapter13.html)

import numpy as np
from plotnine import *
import pandas as pd
from mizani.transforms import trans
from pathlib import Path


# %matplotlib inline


def cleanIparm(dat_dir, pfile, dcol, df, st):
    df1 = pd.read_csv(dat_dir / pfile, header=0)
    ldcol = df1.loc[:, dcol].dropna()  # list with column dcol without NaN
    df.drop(ldcol, axis=1, inplace=True)  # delete params list in dataframes
    st.drop(ldcol, axis=0, inplace=True)
    return df, st


def cleanIparm2(df, st):
    import pandas as pd
    n = len(df.index)
    # ldcol = st.loc[]
    df.drop(st[st['StdDev'] == 0].index, axis=1, inplace=True)
    st.drop(st[st['StdDev'] == 0].index, inplace=True)
    df.drop(st[st['NoModeQty'] == 0].index, axis=1, inplace=True)
    st.drop(st[st['NoModeQty'] == 0].index, inplace=True)
    # parameter removal with high null percentage 
    df.drop(st[st['NaNQty'] > n * .15].index, axis=1, inplace=True)
    st.drop(st[st['NaNQty'] > n * .15].index, inplace=True)
    st.sort_values(by=['IQR', 'CV'], ascending=False)
    return df, st


def iqrcalc(q1, q3, n, std, mean):
    import numpy as np
    if .1 > mean > -.1:
        cv = 100 * std
    else:
        cv = 100 * std / abs(mean)
    return q3 + (1.58 * (q3 - q1) / np.sqrt(n)), q1 - (1.58 * (q3 - q1) / np.sqrt(n)), q3 - q1, cv


# case function for carrier selection. switcher is dictionary data type
def carrtexl(carr):
    switcher = {
        0: 'LTotal',
        1: 'Carrier 2600 I: 3075',
        2: 'Carrier 2600 II: 3225',
        3: 'Carrier 1900 HL: 626',
        4: 'Carrier 1900: 651',
    }
    return switcher.get(carr, 'nothing') # 'nothing' if not found


# case function for carrier selection. switcher is dictionary data type
def carrtext(carr):
    switcher = {
        0: 'UTotal',
        1: 'Carrier I: 4387',
        2: 'Carrier II: 9712',
        3: 'Carrier III: 9685',
        4: 'Carrier IV: 4364',
    }
    return switcher.get(carr, 'nothing') # 'nothing' if not found


# case function for carrier selection. switcher is dictionary data type
def carrierl(carr):
    switcher = {
        0: Uall,
        1: 3075,
        2: 3225,
        3: 626,
        4: 651,
    }
    return switcher.get(carr, 'nothing')


# case function for carrier selection. switcher is dictionary data type
def carriers(carr):
    switcher = {
        0: Lall,
        1: 4387,
        2: 9712,
        3: 9685,
        4: 4364,
    }
    return switcher.get(carr, 'nothing')


def zone(zon):
    switcher = {
        0: 'MED',
        1: 'PER',
        2: 'MAN',
        3: 'ARM',
        4: 'QUB',
        5: 'ANT',
        6: 'RIS',
        7: 'CAD',
        8: 'QUI',
        9: 'CHO',
    }
    return switcher.get(zon, 'nothing')


def par_audit(df):
    import functools
    n = len(df.index)  # row count
    # mode stored in columns
    modes = df.mode(dropna=False)
    # dummy rows delete
    modes = modes.dropna(subset=['Encargado'])
    # dictionaries. data (count values diff from mode in modes) data1 (count of values = mode in modes)
    data = {col: (~df[col].isin(modes[col])).sum() for col in df.iloc[:, 0:].columns}
    data1 = {col: df[col].isin(modes[col]).sum() for col in df.iloc[:, 0:].columns}
    # st3 mode info
    st3 = pd.DataFrame.from_dict(data, orient='index', columns=['NoModeQty'])
    st3['ModeQty'] = pd.DataFrame.from_dict(data1, orient='index')
    st3['NoModePer'] = 100 * (st3['NoModeQty'] / (st3['ModeQty'] + st3['NoModeQty']))
    st3.index.name = 'parameter'
    st2 = modes.T
    st2.columns = ['Mode']
    st2.index.name = 'parameter'
    st1 = pd.DataFrame({'Vmin': df.min(), 'StdDev': df.std(), 'NaNQty': df.isnull().sum(axis=0), 'Mean': df.mean(),
                        'Q1': df.quantile(.25), 'Q3': df.quantile(.75), 'Median': df.quantile(.5)})
    st1[['Max', 'Min', 'IQR', 'CV']] = st1.apply(lambda row: iqrcalc(row['Q1'], row['Q3'], n, row['StdDev'],
                                                                     row['Mean']), axis=1, result_type='expand')
    st1.index.name = 'parameter'
    # df merge
    dfs = [st1, st2, st3]
    st4 = functools.reduce(lambda left, right: pd.merge(left, right, on='parameter'), dfs)
    st4.sort_values(by=['IQR', 'CV'], inplace=True, ascending=[False, False])
    return st4


def statzon(df):
    dftemp = df.reset_index(level=(0, 1))
    stzf=[]
    n = 10  # zone number
    for i in range(0, n):  # loop for each zone
        area = zone(i)
        dfzi = dftemp[:][dftemp.Prefijo == area]  # data per zone
        if len(dfzi) > 0: # control for empty df
            if i == 0:
                stzf = par_audit(dfzi)
                stzf['Prefijo'] = area
            else:
                stz = par_audit(dfzi)
                stz['Prefijo'] = area
                if len(stzf) == 0:  # empty stzf control
                    stzf = stz
                else:
                    stzf = stzf.append(stz)
    return stzf


class asinh_trans(trans):
    """
        asinh Transformation
        """

    @staticmethod
    def transform(y):
        y = np.asarray(y)
        return np.arcsinh(y)

    @staticmethod
    def inverse(y):
        y = np.asarray(y)
        return np.sinh(y)


def pntopd(file, figs, x, y, wi, he):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, letter, landscape, portrait
    w, h = letter
    c = canvas.Canvas(str(file), pagesize=portrait(letter))
    for png in figs:
        c.drawImage(png, x, h - y, width=wi, height=he)
        c.showPage()
    c.save()


def par_aud(ruta, datb, tablas, tipo):
    import numpy as np
    from pyexcelerate import Workbook
    from pyexcelerate_to_excel import pyexcelerate_to_excel
    from datetime import date
    import sqlite3

    dat_dir = Path(ruta)
    db_path1 = dat_dir / datb
    conn = sqlite3.connect(db_path1)  # database connection
    c = conn.cursor()
    df1 = pd.read_csv(dat_dir / tablas)
    today = date.today()
    xls_file = tipo + today.strftime("%y%m%d") + ".xlsx"
    xls_path = dat_dir / xls_file  # xls file path-name
    wb = Workbook()  # pyexcelerate Workbook
    for index, row in df1.iterrows():  # table row iteration by audit2 column type
        line = row[tipo]
        if not pd.isna(row[tipo]):  # nan null values validation
            if line == 'LNBTS':
                pnglist = []
                tit = today.strftime("%y%m%d") + '_ParameterAudit'
                xls_file = tit + ".xlsx"
                xls_path = dat_dir / xls_file
                pdf_file = tit + ".pdf"
                pdf_path = dat_dir / pdf_file
                if line == 'LNCEL' or line == 'WCEL' : # carrier count - amount of graphs 1 for BTS
                    n = 5
                elif line == 'LNBTS':
                    n = 1
                for i in range(0, n):  # loop for each carrier
                    if line == 'LNBTS':
                        carr = 'LNBTS'
                        cart = ''
                    elif line == 'LNCEL':
                        carr = carrierl(i) # carrier number
                        cart = carrtexl(i)
                    elif line == 'WCEL':
                        carr = carriers(i)
                        cart = carrtext(i)
                    try:
                        if line == 'LNBTS':
                            df = pd.read_sql_query("select * from LNBTS_Full;", conn, index_col=['LNBTSname', 'Prefijo'])
                        elif line == 'LNCEL':
                            if carr == Lall:
                                df = pd.read_sql_query("select * from LNCEL_Full;", conn, index_col=['LNCELname', 'Prefijo'])
                            else:
                                df = pd.read_sql_query("select * from LNCEL_Full where (earfcnDL = " + str(carr) + ");",
                                                       conn, index_col=['LNCELname', 'Prefijo'])
                            df = df.dropna(subset=['Banda'])   # drop rows with band nan
                        elif line == 'WCEL':
                            if carr == Uall:
                                df = pd.read_sql_query("select * from WCEL_FULL1;", conn, index_col=['WCELName', 'Prefijo'])
                            else:
                                df = pd.read_sql_query("select * from WCEL_FULL1 where (UARFCN = " + str(carr) + ");",
                                                       conn, index_col=['WCELName', 'Prefijo'])
                        stpref = statzon(df)  # stats per parameter and prefijo
                        st = par_audit(df)  # stats per parameter full set
                        output = 'parametros.csv'
                        st.to_csv(dat_dir / output)
                        if line == 'LNBTS':
                            df, st = cleanIparm(dat_dir, "ExParam.csv", "explwbt", df, st)  # info parameter removal
                        elif line == 'LNCEL':
                            df, st = cleanIparm(dat_dir, "ExParam.csv", "explcel", df, st)  # info parameter removal
                        elif line == 'WCEL':
                            df, st = cleanIparm(dat_dir, "ExParam.csv", "expar", df, st)  # info parameter removal
                        pyexcelerate_to_excel(wb, st, sheet_name= str(carr), index=True)
                        df, st = cleanIparm2(df, st)  # standardized params and NaN>0.15*n removal
                        st['topdisc'] = range(len(st))  # top disc counter by IQR-CV
                        st['topdisc'] = st['topdisc'].floordiv(10)  # split disc in groups by 10
                        st.sort_values(by=['Median'], inplace=True, ascending=[False])  # for better visualization
                        st['counter'] = range(len(st))  # counter controls number of boxplots
                        st['counter'] = st['counter'].floordiv(10)  # split parameters in groups by 10
                        cols = ['StdDev', 'Mean', 'Median', 'Max', 'Min', 'CV']
                        st[cols] = st[cols].round(1)  # scales colums with 1 decimal digit
                        stpref[cols] = stpref[cols].round(1) # Prefijo info
                        # concat info to put text in boxplots
                        st['concat'] = st['StdDev'].astype(str) + ', ' + st['NoModeQty'].astype(str)
                        stpref['concat'] = stpref['StdDev'].astype(str) + ', ' + stpref['NoModeQty'].astype(str)
                        ldcol = list(st.index)  # parameters to include in melt command
                        # Structuring df1 according to ‘tidy data‘ standard
                        df.reset_index(level=(0, 1), inplace=True)  # to use indexes in melt operation
                        df1 = df.melt(id_vars=['Prefijo'], value_vars=ldcol,  # WCELName is not used
                                      var_name='parameter', value_name='value')
                        df1 = df1.dropna(subset=['value'])  # drop rows with value NaN
                        st.reset_index(inplace=True)  # parameter from index to col
                        stpref.reset_index(inplace=True)  # parameter from index to col
                        temp = st[['parameter', 'topdisc']] # topdisc to be included in stpref
                        stpref = pd.merge(stpref, temp, on='parameter')
                        result = pd.merge(df1, st, on='parameter')  # merge by columns not by index
                        resultzon = pd.merge(df1, stpref, on=['parameter', 'Prefijo'])  # merge by columns not by index
#                         out1 = "C" + str(carr) + ".csv"
#                         out2 = "D" + str(carr) + ".csv"
#                         out3 = "E" + str(carr) + ".csv"
#                         out4 = "F" + str(carr) + ".csv"
#                         st.to_csv(dat_dir / out1)
#                         stpref.to_csv(dat_dir / out2)
#                         result.to_csv(dat_dir / out3)
#                         resultzon.to_csv(dat_dir / out4)
                        # graph code
                        custom_axis = theme(axis_text_x=element_text(color="grey", size=6, angle=90, hjust=.3),
                                            axis_text_y=element_text(color="grey", size=6),
                                            plot_title=element_text(size=25, face="bold"),
                                            axis_title=element_text(size=10),
                                            panel_spacing_x=1.6, panel_spacing_y=.45,
                                            # 2nd value number of rows and colunms
                                            figure_size=(5 * 4, 3.5 * 4)
                                            )
                        # ggplot code:value 'concat' is placed in coordinate (parameter, stddev)
                        my_plot = (ggplot(data=result, mapping=aes(x='parameter', y='value')) + geom_boxplot() +
                                   geom_text(data=st, mapping=aes(x='parameter', y='StdDev', label='concat'),
                                             color='red', va='top', ha='left', size=7, nudge_x=.6, nudge_y=-1.5) +
                                   facet_wrap('counter', scales='free') + custom_axis + scale_y_continuous(
                                    trans=asinh_trans) + ylab("Values") + xlab("Parameters") +
                                   labs(title=line + " Parameter Audit " + cart) + coord_flip())
                        pngname = str(carr) + ".png" # saveplot
                        pngfile = dat_dir / pngname
                        my_plot.save(pngfile, width=20, height=10, dpi=300)
                        pnglist.append(pngfile) # plots to be printed in pdf
                        n = 2 # top 2 plots
                        for j in range(0, n):
                            toplot = resultzon.loc[resultzon['topdisc'] == j] # filter info for parameter set to be printed
                            toplot1 = stpref.loc[stpref['topdisc'] == j]
                            custom_axis = theme(axis_text_x=element_text(color="grey", size=7, angle=90, hjust=.3),
                                                axis_text_y=element_text(color="grey", size=7),
                                                plot_title=element_text(size=25, face="bold"),
                                                axis_title=element_text(size=10),
                                                panel_spacing_x=0.6, panel_spacing_y=.45,
                                                # 2nd value number of rows and colunms
                                                figure_size=(5 * 4, 3.5 * 4)
                                                )
                            top_plot = (ggplot(data=toplot, mapping=aes(x='parameter', y='value')) + geom_boxplot() +
                                        geom_text(data=toplot1, mapping=aes(x='parameter', y='StdDev', label='concat'),
                                                  color='red', va='top', ha='left', size=7, nudge_x=.6, nudge_y=-1.5) +
                                        facet_wrap('Prefijo') + custom_axis + scale_y_continuous(
                                        trans=asinh_trans) + ylab("Values") + xlab("Parameters") +
                                        labs(title="Top " + str(j+1) + " Disc Parameter per Zone. " + cart) + coord_flip())
                            pngname = str(carr) + str(j+1) + ".png"
                            pngfile = dat_dir / pngname
                            top_plot.save(pngfile, width=20, height=10, dpi=300)
                            pnglist.append(pngfile)
                    except sqlite3.Error as error:  # sqlite error handling.
                        print('SQLite error: %s' % (' '.join(error.args)))
                        feedbk = tk.Label(top, text='SQLite error: %s' % (' '.join(error.args)))
                        feedbk.pack()
    wb.save(xls_path)
    pntopd(pdf_path, pnglist, 50, 550, 500, 500)
    c.close()
    conn.close()


par_aud("C:/SQLite", "20200522_sqlite.db", "tablasSQL.csv", "audit2")  # audit2 column from csv table file




