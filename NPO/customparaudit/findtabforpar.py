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


from plotnine import *
from mizani.transforms import trans
import numpy as np
from rfpack.validatabc import validatab


def statzon(df):
    from rfpack.zonec import zone
    # from rfpack.par_auditc import par_audit

    df = df.copy(deep=True)    # Modifications to the data of the copy wont be reflected in the orig object
    dftemp = df.reset_index()
    # dftemp = df.reset_index(level=(0, 1))
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


def znfrmt(seq):
    switcher = {
        0: ['full', 'MED', 'ANT'],
        1: ['PER', 'MAN', 'ARM'],
        2: ['RIS', 'CAD', 'QUI'],
        3: ['QUB', 'CHO'],
    }
    return switcher.get(seq, 'nothing')

# +
# def percentile(n):
#     def percentile_(x):
#         return np.percentile(x, n)
#     percentile_.__name__ = 'percentile_%s' % n
#     return percentile_
# -

def par_audit(df):
    import functools
    import pandas as pd
    from rfpack.iqrcalcc import iqrcalc

    df = df.copy(deep=True)  # Modifications to the data of the copy wont be reflected in the orig object
    # n = len(df.index)  # row count
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
    # st3.index.name = 'parameter'
    st2 = modes.T
    st2.columns = ['Mode']
    # st2.index.name = 'parameter'
    st2 = st2.merge(st3, how='left', left_index=True, right_index=True)
    # st1 = pd.DataFrame({'Vmin': df.min(), 'StdDev': df.std(), 'NaNQty': df.isnull().sum(axis=0), 'Mean': df.mean(),
    #                     'Q1': df.quantile(.25), 'Q3': df.quantile(.75), 'Median': df.quantile(.5)})
    # st1[['Max', 'Min', 'IQR', 'CV']] = st1.apply(lambda row: iqrcalc(row['Q1'], row['Q3'], n, row['StdDev'],
    #                                                                  row['Mean']), axis=1, result_type='expand')
    df2 = df.describe().T
    df2.rename(columns={'25%': 'Q1', '50%': 'Median', '75%': 'Q3', 'std': 'StdDev',
                        'count': 'n', 'min': 'Vmin'}, inplace=True)
    st1 = pd.DataFrame({'NaNQty': df.isnull().sum(axis=0)})
    st1 = df2.merge(st1, how='left', left_index=True, right_index=True)
    st1[['upper', 'lower', 'IQR', 'CV']] = st1.apply(lambda row: iqrcalc(row['Q1'], row['Q3'], row['n'], row['StdDev'],
                                                                     row['mean']), axis=1, result_type='expand')
    st4 = st1.merge(st2, how='left', left_index=True, right_index=True)
    st4.index.name = 'parameter'
    # dfs = [st1, st2, st3]
    # st4 = functools.reduce(lambda left, right: pd.merge(left, right, on='parameter'), dfs)
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


# +
# def cleaniparm(dat_dir, pfile, dcol, df, st):
#     import pandas as pd
#     df = df.copy(deep=True)  # Modifications to the data of the copy wont be reflected in the orig object
#     df8 = pd.read_csv(dat_dir / pfile, header=0)
#     ldcol = df8.loc[:, dcol].dropna()  # list with column dcol without NaN
#     df.drop(ldcol, axis=1, inplace=True)  # delete params list in dataframes
#     st.drop(ldcol, axis=0, inplace=True)
#     return df, st
# -


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
    consfull = []
    conspref = []
    tit = today.strftime("%y%m%d") + '_Feat1ParAudit'
    xls_file = tit + ".xlsx"
    xls_path = dat_dir / xls_file
    pdf_file = tit + ".pdf"
    pdf_path = dat_dir / pdf_file
    conn = sqlite3.connect(db_path1)  # database connection
    c = conn.cursor()
    ftab1 = tab_par + '.csv'  # tables and parameters to audit
    df3 = pd.read_csv(dat_dir / ftab1)
    df4 = df3.groupby('table_name')['parameter'].apply(list).reset_index(name='parlist')
    for index, row in df4.iterrows(): # table row iteration
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
            paramsext = ('Prefijo', 'WBTS_id', 'UARFCN', 'WCELName', 'Banda', 'Encargado')
            namtoinx = 'WCELName'
            carrfilt = 'UARFCN'
        elif line == 'ANRPRL':
            paramsext = ('Prefijo', 'LNBTS_id', 'LNBTSname', 'Banda', 'Encargado')
            namtoinx = 'LNBTSname'
            carrfilt = 'targetCarrierFreq'
        elif line == 'RNFC':
            paramsext = ('Prefijo', 'RNC_id', 'RNCName', 'Encargado')
            namtoinx = 'RNCName'
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
        try:  # include queries for all and carrier, pending
            datsrc = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                                       index_col=[namtoinx, 'Prefijo'])
            pyexcelerate_to_excel(wb, datsrc, sheet_name=line + '_data', index=True)
            output = 'paramfull.csv'
            datsrc.to_csv(dat_dir / output)
            if not (line == 'LNBTS' or line == 'RNFC' or line == 'WBTS'):
                datsrc = datsrc.dropna(subset=['Banda'])
            for i in range(0, n):  # loop for each carrier. once for no carrier tables
                if line == 'WCEL':
                    carr = carriers(i)
                    cart = carrtext(i)
                # elif line == 'ANRPRL':
                #     carr = carrierl(i)  # carrier number
                #     cart = carrtexl(i)
                else:   # add columns to include in table query
                    carr = carrierl(i)  # carrier number
                    cart = carrtexl(i)
                    # if line == 'LNBTS' or line == 'RNFC' or line == 'WBTS':
                    #     df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                    #                            index_col=[namtoinx, 'Prefijo'])
                    # else:  # 11 carrier related tables
                    #     if carr == 'all':
                    #         df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                    #                                index_col=[namtoinx, 'Prefijo'])
                    #     else:
                    #         df = pd.read_sql_query("select " + parstring + " from " + tabsq + " where (" + str(carrfilt) + " = " + str(carr) + ");",
                    #                                conn, index_col=[namtoinx, 'Prefijo'])
                    #     df = df.dropna(subset=['Banda'])  # drop rows with band nan REVIEW IF NECESSARY
    #                 print(df) # continue to process
                if line == 'LNBTS' or line == 'RNFC' or line == 'WBTS' or carr == 'all':
                    df2 = datsrc
                else:
                    df2 = datsrc[:][datsrc[carrfilt] == carr]
                if len(df2) > 0:  # control for empty df
                    stpref = statzon(df2)  # stats per parameter and prefijo
                    st = par_audit(df2)  # stats per parameter full set
                    output = 'parametros.csv'
                    st.to_csv(dat_dir / output)
                    output = 'parametro.csv'
                    stpref.to_csv(dat_dir / output)
                    df2, st = cleaniparm(dat_dir, "ExParam.csv", "expfeat1", df2, st)  # info parameter removal
                    if line == 'LNBTS' or line == 'RNFC' or line == 'WBTS' or carr == 'all':
                        sttemp = st.copy(deep=True)
                        sttemp.insert(0, 'table', line)
                        sttemp1 = stpref.copy(deep=True)
                        sttemp1.insert(0, 'table', line)
                        if len(consfull) == 0:  # empty stzf control
                            consfull = sttemp
                        else:
                            consfull = consfull.append(sttemp)
                        if len(conspref) == 0:  # empty stzf control
                            conspref = sttemp1
                        else:
                            conspref = conspref.append(sttemp1)
                    else:
                        pyexcelerate_to_excel(wb, st, sheet_name=line + str(carr), index=True)
                        pyexcelerate_to_excel(wb, stpref, sheet_name=line + str(carr) + 'pref', index=True)
                    df2, st = cleaniparm2(df2, st)  # standardized params and NaN>0.15*n removal
                    parqty = len(st)   # parameter amount
                    if parqty > 0: # only for parameters with discrepancies
                        st['topdisc'] = range(parqty)  # top disc counter by IQR-CV
                        st['topdisc'] = st['topdisc'].floordiv(10)  # split disc in groups by 10
                        st.sort_values(by=['Median'], inplace=True, ascending=[False])  # for better visualization
                        st['counter'] = range(parqty)  # counter controls number of boxplots
                        st['counter'] = st['counter'].floordiv(10)  # split parameters in groups by 10
                        cols = ['StdDev', 'mean', 'Median', 'upper', 'lower', 'CV']
                        st[cols] = st[cols].round(1)  # scales colums with 1 decimal digit
                        stpref[cols] = stpref[cols].round(1)  # Prefijo info
                        # concat info to put text in boxplots
                        st['concat'] = st['StdDev'].astype(str) + ', ' + st['NoModeQty'].astype(str)
                        stpref['concat'] = stpref['StdDev'].astype(str) + ', ' + stpref['NoModeQty'].astype(str)
                        ldcol = list(st.index)  # parameters to include in melt command
                        # Structuring df2 according to ‘tidy data‘ standard
                        df2 = df2.reset_index()  # to use indexes in melt operation
                        # df.reset_index(level=(0, 1), inplace=True)  # to use indexes in melt operation
                        df1 = df2.melt(id_vars=['Prefijo'], value_vars=ldcol,  # WCELName is not used
                                       var_name='parameter', value_name='value')
                        df1 = df1.dropna(subset=['value'])  # drop rows with value NaN
                        st.reset_index(inplace=True)  # parameter from index to col
                        stpref.reset_index(inplace=True)  # parameter from index to col
                        temp = st[['parameter', 'topdisc']]  # topdisc to be included in stpref
                        stpref = pd.merge(stpref, temp, on='parameter')
                        result = pd.merge(df1, st, on='parameter')  # merge by columns not by index
                        resultzon = pd.merge(df1, stpref, on=['parameter', 'Prefijo'])  # merge by columns not by index
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
                        pngname = str(line) + str(carr) + ".png"  # saveplot
                        pngfile = dat_dir / pngname
                        my_plot.save(pngfile, width=20, height=10, dpi=300)
                        pnglist.append(pngfile)  # plots to be printed in pdf
                        if parqty < 11:
                            n = 1  # only 1 plot
                        else:
                            n = 2  # top 2 plots
                        for j in range(0, n):
                            toplot = resultzon.loc[resultzon['topdisc'] == j]  # filter info for parameter set to be printed
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
                                        labs(title="Top " + str(j + 1) + " Disc Parameter per Zone. " + cart) + coord_flip())
                            pngname = str(line) + str(carr) + str(j + 1) + ".png"
                            pngfile = dat_dir / pngname
                            top_plot.save(pngfile, width=20, height=10, dpi=300)
                            pnglist.append(pngfile)
        except sqlite3.Error as error:  # sqlite error handling.
            print('SQLite error: %s' % (' '.join(error.args)))
            # feedbk = tk.Label(top, text='SQLite error: %s' % (' '.join(error.args)))
            # feedbk.pack()
    filterpar = list(df3.parameter)
    consfull = consfull.reset_index().rename(columns={'index': 'parameter'})
    consfull['Prefijo'] = 'full'
    conspref = conspref.reset_index().rename(columns={'index': 'parameter'})
    consfull = consfull.append(conspref, ignore_index = True)  # consfull info to show CV and nomodeper
    consfull = consfull[consfull['parameter'].isin(filterpar)]  # includes only input parameters
    consfull.dropna(subset=['CV'], inplace=True)
    for index, row in consfull.iterrows():  # table row iteration by Prefijo column type
        if row['Prefijo'] in znfrmt(0):
            consfull.loc[index, 'prorder'] = 0  # update column with print order id
        elif row['Prefijo'] in znfrmt(1):
            consfull.loc[index, 'prorder'] = 1
        elif row['Prefijo'] in znfrmt(2):
            consfull.loc[index, 'prorder'] = 2
        else:
            consfull.loc[index, 'prorder'] = 3
    pyexcelerate_to_excel(wb, consfull, sheet_name='Total', index=False)
    wb.save(xls_path)
    pntopd(pdf_path, pnglist, 50, 550, 500, 500)
    c.close()
    conn.close()


validatab('C:/SQLite', '20200522_sqlite.db', 'findtable', 'tabcustom')
customparam('C:/SQLite', '20200522_sqlite.db', 'tab_par')


