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

# # par_aud
# . provides pdf with parame tert audit.
# . for tables LNBTS, LNCEL, WBTS y WCEL

def par_aud(ruta, datb, tablas, tipo):
    import pandas as pd
    from mizani.transforms import trans
    import numpy as np
    from pyexcelerate import Workbook
    from pyexcelerate_to_excel import pyexcelerate_to_excel
    from datetime import date
    import sqlite3
    from plotnine import *
    from pathlib import Path

    dat_dir = Path(ruta)
    db_path1 = dat_dir / datb
    conn = sqlite3.connect(db_path1)  # database connection
    c = conn.cursor()
    df1 = pd.read_csv(dat_dir / tablas)
    today = date.today()
    xls_file = tipo + today.strftime("%y%m%d") + ".xlsx"
    xls_path = dat_dir / xls_file  # xls file path-name
    wb = Workbook()  # pyexcelerate Workbook
    pnglist = []
    tit = today.strftime("%y%m%d") + '_ParameterAudit'
    xls_file = tit + ".xlsx"
    xls_path = dat_dir / xls_file
    pdf_file = tit + ".pdf"
    pdf_path = dat_dir / pdf_file
    for index, row in df1.iterrows():  # table row iteration by audit2 column type
        line = row[tipo]
        if not pd.isna(row[tipo]):  # nan null values validation
            if line == 'LNCEL' or line == 'WCEL' : # carrier count - amount of graphs 1 for BTS
                n = 5
            elif line == 'LNBTS' or line == 'WBTS' :
                n = 1
            for i in range(0, n):  # loop for each carrier
                if line == 'LNBTS' or line == 'WBTS':
                    cart = ''
                    if line == 'LNBTS':
                        carr = 'LNBTS'
                    else:
                        carr = 'WBTS'
                elif line == 'LNCEL':
                    carr = carrierl(i) # carrier number
                    cart = carrtexl(i)
                elif line == 'WCEL':
                    carr = carriers(i)
                    cart = carrtext(i)
                try:
                    if line == 'LNBTS':
                        df = pd.read_sql_query("select * from LNBTS_Full;", conn, index_col=['LNBTSname', 'Prefijo'])
                    elif line == 'WBTS':
                        df = pd.read_sql_query("select * from WBTS_Full1;", conn, index_col=['WBTSName', 'Prefijo'])
                    elif line == 'LNCEL':
                        if carr == 'Lall':
                            df = pd.read_sql_query("select * from LNCEL_Full;", conn, index_col=['LNCELname', 'Prefijo'])
                        else:
                            df = pd.read_sql_query("select * from LNCEL_Full where (earfcnDL = " + str(carr) + ");",
                                                   conn, index_col=['LNCELname', 'Prefijo'])
                        df = df.dropna(subset=['Banda'])   # drop rows with band nan
                    elif line == 'WCEL':
                        if carr == 'Uall':
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
                    elif line == 'WBTS':
                        df, st = cleanIparm(dat_dir, "ExParam.csv", "expwbts", df, st)  # info parameter removal
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
