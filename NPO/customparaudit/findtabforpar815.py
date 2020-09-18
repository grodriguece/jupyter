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

# # Find Table for Parameter List
# tabcustom.csv: custom tables created not included in table find analysis<br> 
# make a list for each table in order to sent to sql query<br>
# 10 parameter per group<br>
# line will take table name
#
#
#


from rfpack.validatabc import validatab
from plotnine import *
from mizani.transforms import trans
import numpy as np


def statzon(df):
    from rfpack.zonec import zone
    # from rfpack.par_auditc import par_audit

    dftemp = df.reset_index(level=(0, 1))
    stzf = []
    n = 10  # zone number
    for i in range(0, n):  # loop for each zone
        area = zone(i)
        dfzi = dftemp[:][dftemp.Prefijo == area]  # data per zone
        if len(dfzi) > 0:  # control for empty df
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


def par_audit(df):
    import functools
    import pandas as pd
    from rfpack.iqrcalcc import iqrcalc

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


def customparam(ruta, datb, tab_par):
    import pandas as pd
    from pathlib import Path
    from datetime import date
    import sqlite3
    from pyexcelerate import Workbook
    from pyexcelerate_to_excel import pyexcelerate_to_excel
    # from pyexcelerate_to_excel import Workbook
    from rfpack.carriersc import carriers
    from rfpack.carrierlc import carrierl
    from rfpack.carrtextc import carrtext
    from rfpack.carrtexlc import carrtexl
    # from rfpack.statzonc import statzon
    # from rfpack.par_auditc import par_audit
    from rfpack.cleaniparmc import cleaniparm
    from rfpack.cleaniparm2c import cleaniparm2
    from rfpack.pntopdc import pntopd
    from rfpack.tabconvc import tabconv

    dat_dir = Path(ruta)
    db_path1 = dat_dir / datb
    today = date.today()
    wb = Workbook()  # pyexcelerate Workbook
    pnglist = []
    tit = today.strftime("%y%m%d") + '_Feat1ParAudit'
    xls_file = tit + ".xlsx"
    xls_path = dat_dir / xls_file
    pdf_file = tit + ".pdf"
    pdf_path = dat_dir / pdf_file
    conn = sqlite3.connect(db_path1)  # database connection
    c = conn.cursor()
    ftab1 = tab_par + '.csv'  # tables and parameters to audit
    df = pd.read_csv(dat_dir / ftab1)
    df1 = df.groupby('table_name')['Parameter'].apply(list).reset_index(name='parlist')
    for index, row in df1.iterrows(): # table row iteration
        # print(row['table_name'], row['parlist'])
        line = row['table_name']
        namtoinx = 'LNCELname'    # default values for lncel related tables
        carrfilt = 'earfcnDL'
        if line == 'RNFC' or line == 'LNBTS':  # carrier count - amount of graphs 1 for BTS
            n = 1    # 2 individual tables
        else:
            n = 5   # 11 tables with carries to graph
        paramst1 = row['parlist']  # parameter list
        if line == 'WCEL':
            paramsext = ('Prefijo', 'WBTS_id', 'UARFCN', 'WCELname', 'Banda', 'Encargado')
            namtoinx = 'WCELname'
            carrfilt = 'UARFCN'
        elif line == 'ANRPRL':
            paramsext = ('Prefijo', 'LNBTS_id', 'LNBTSname', 'Banda', 'Encargado')
            namtoinx = 'LNBTSname'
            carrfilt = 'targetCarrierFreq'
        elif line == 'RNFC':
            paramsext = ('Prefijo', 'RNC_id', 'RNCname', 'Encargado')
            namtoinx = 'RNCname'
            carr = 'RNC'
        elif line == 'LNBTS':
            paramsext = ('Prefijo', 'LNBTSname', 'Encargado')
            namtoinx = 'LNBTSname'
            carr = 'LNBTS'
        else:  # add columns to include in table query
            paramsext = ('Prefijo', 'LNBTS_id', 'earfcnDL', 'LNCELname', 'Banda', 'Encargado')
        paramst1.extend(paramsext)
        parstring = ','.join(paramst1)
        tabsq = tabconv(line)  # select reference table to get info
        for i in range(0, n):  # loop for each carrier
            if line == 'WCEL':
                carr = carriers(i)
                cart = carrtext(i)
            elif line == 'ANRPRL':
                carr = carrierl(i)  # carrier number
                cart = carrtexl(i)
            else:   # add columns to include in table query
                carr = carrierl(i)  # carrier number
                cart = carrtexl(i)
            try:  # include queries for all and carrier, pending
                if line == 'LNBTS' or line == 'RNFC' or line == 'WBTS':
                    df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                                           index_col=[namtoinx, 'Prefijo'])
                else:  # 11 carrier related tables
                    if carr == 'all':
                        df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                                               index_col=[namtoinx, 'Prefijo'])
                    else:
                        df = pd.read_sql_query("select " + parstring + " from " + tabsq + " where (" + str(carrfilt) + " = " + str(carr) + ");",
                                               conn, index_col=[namtoinx, 'Prefijo'])
                    df = df.dropna(subset=['Banda'])  # drop rows with band nan REVIEW IF NECESSARY
#                 print(df) # continue to process
                if len(df) > 0:  # control for empty df
                    stpref = statzon(df)  # stats per parameter and prefijo
                    st = par_audit(df)  # stats per parameter full set
                    output = 'parametros.csv'
                    st.to_csv(dat_dir / output)
                    df, st = cleaniparm(dat_dir, "ExParam.csv", "expfeat1", df, st)  # info parameter removal
                    pyexcelerate_to_excel(wb, st, sheet_name=line + str(carr), index=True)
                    df, st = cleaniparm2(df, st)  # standardized params and NaN>0.15*n removal
                    parqty = len(st)   # parameter amount
                    st['topdisc'] = range(parqty)  # top disc counter by IQR-CV
                    st['topdisc'] = st['topdisc'].floordiv(10)  # split disc in groups by 10
                    st.sort_values(by=['Median'], inplace=True, ascending=[False])  # for better visualization
                    st['counter'] = range(parqty)  # counter controls number of boxplots
                    st['counter'] = st['counter'].floordiv(10)  # split parameters in groups by 10
                    cols = ['StdDev', 'Mean', 'Median', 'Max', 'Min', 'CV']
                    st[cols] = st[cols].round(1)  # scales colums with 1 decimal digit
                    stpref[cols] = stpref[cols].round(1)  # Prefijo info
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
                    temp = st[['parameter', 'topdisc']]  # topdisc to be included in stpref
                    stpref = pd.merge(stpref, temp, on='parameter')
                    result = pd.merge(df1, st, on='parameter')  # merge by columns not by index
                    resultzon = pd.merge(df1, stpref, on=['parameter', 'Prefijo'])  # merge by columns not by index
                    # graph code
                    # custom_axis = theme(axis_text_x=element_text(color="grey", size=6, angle=90, hjust=.3),
                    #                     axis_text_y=element_text(color="grey", size=6),
                    #                     plot_title=element_text(size=25, face="bold"),
                    #                     axis_title=element_text(size=10),
                    #                     panel_spacing_x=1.6, panel_spacing_y=.45,
                    #                     # 2nd value number of rows and colunms
                    #                     figure_size=(5 * 4, 3.5 * 4)
                    #                     )
                    # # ggplot code:value 'concat' is placed in coordinate (parameter, stddev)
                    # my_plot = (ggplot(data=result, mapping=aes(x='parameter', y='value')) + geom_boxplot() +
                    #            geom_text(data=st, mapping=aes(x='parameter', y='StdDev', label='concat'),
                    #                      color='red', va='top', ha='left', size=7, nudge_x=.6, nudge_y=-1.5) +
                    #            facet_wrap('counter', scales='free') + custom_axis + scale_y_continuous(
                    #             trans=asinh_trans) + ylab("Values") + xlab("Parameters") +
                    #            labs(title=line + " Parameter Audit " + cart) + coord_flip())
                    # pngname = str(carr) + ".png"  # saveplot
                    # pngfile = dat_dir / pngname
                    # my_plot.save(pngfile, width=20, height=10, dpi=300)
                    # pnglist.append(pngfile)  # plots to be printed in pdf
                    # if parqty < 11:
                    #     n = 1  # only 1 plot
                    # else:
                    #     n = 2  # top 2 plots
                    # for j in range(0, n):
                    #     toplot = resultzon.loc[resultzon['topdisc'] == j]  # filter info for parameter set to be printed
                    #     toplot1 = stpref.loc[stpref['topdisc'] == j]
                    #     custom_axis = theme(axis_text_x=element_text(color="grey", size=7, angle=90, hjust=.3),
                    #                         axis_text_y=element_text(color="grey", size=7),
                    #                         plot_title=element_text(size=25, face="bold"),
                    #                         axis_title=element_text(size=10),
                    #                         panel_spacing_x=0.6, panel_spacing_y=.45,
                    #                         # 2nd value number of rows and colunms
                    #                         figure_size=(5 * 4, 3.5 * 4)
                    #                         )
                    #     top_plot = (ggplot(data=toplot, mapping=aes(x='parameter', y='value')) + geom_boxplot() +
                    #                 geom_text(data=toplot1, mapping=aes(x='parameter', y='StdDev', label='concat'),
                    #                           color='red', va='top', ha='left', size=7, nudge_x=.6, nudge_y=-1.5) +
                    #                 facet_wrap('Prefijo') + custom_axis + scale_y_continuous(
                    #                 trans=asinh_trans) + ylab("Values") + xlab("Parameters") +
                    #                 labs(title="Top " + str(j + 1) + " Disc Parameter per Zone. " + cart) + coord_flip())
                    #     pngname = str(carr) + str(j + 1) + ".png"
                    #     pngfile = dat_dir / pngname
                    #     top_plot.save(pngfile, width=20, height=10, dpi=300)
                    #     pnglist.append(pngfile)
            except sqlite3.Error as error:  # sqlite error handling.
                print('SQLite error: %s' % (' '.join(error.args)))
                feedbk = tk.Label(top, text='SQLite error: %s' % (' '.join(error.args)))
                feedbk.pack()
    wb.save(xls_path)
    # pntopd(pdf_path, pnglist, 50, 550, 500, 500)
    c.close()
    conn.close()


validatab('C:/SQLite', '20200522_sqlite.db', 'findtable', 'tabcustom')
customparam('C:/SQLite', '20200522_sqlite.db', 'tab_par')

