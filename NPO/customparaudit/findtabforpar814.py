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
# tabcustom.csv: custom tables created not included in table find analysis.
#
# make a list for each table in order to sent to sql query.
# 10 parameter per group.
# line will take table name.
#
#
#


from rfpack.validatabc import validatab


def customparam(ruta, datb, tab_par):
    import pandas as pd
    from pathlib import Path
    from datetime import date
    import sqlite3
    # from pyexcelerate import Workbook
    from pyexcelerate_to_excel import pyexcelerate_to_excel
    from pyexcelerate_to_excel import Workbook
    from rfpack.carriersc import carriers
    from rfpack.carrierlc import carrierl
    from rfpack.carrtextc import carrtext
    from rfpack.carrtexlc import carrtexl
    from rfpack.statzonc import statzon
    from rfpack.par_auditc import par_audit
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
    df1 = df.groupby('table_name')['parameter'].apply(list).reset_index(name='parlist')
    for index, row in df1.iterrows(): # table row iteration
        # print(row['table_name'], row['parlist'])
        line = row['table_name']
        namtoinx = 'LNCELname'    # default values for lncel related tables
        carrfilt = 'earfcnDL'
        if line == 'RNFC' or line == 'LNBTS':  # carrier count - amount of graphs 1 for BTS
            n = 1    # 2 individual tables
        else:
            n = 5   # 11 tables with carries to graph
        for i in range(0, n):  # loop for each carrier
            paramst1 = row['parlist']  # parameter list
            if line == 'WCEL':
                paramsext = ('Prefijo', 'WBTS_id', 'UARFCN', 'WCELname', 'Banda')
                carr = carriers(i)
                cart = carrtext(i)
                namtoinx = 'WCELname'
                carrfilt = 'UARFCN'
            elif line == 'ANRPRL':
                paramsext = ('Prefijo', 'LNBTS_id', 'targetCarrierFreq', 'LNBTSname', 'Banda')
                carr = carrierl(i)  # carrier number
                cart = carrtexl(i)
                namtoinx = 'LNBTSname'
                carrfilt = 'targetCarrierFreq'
            elif line == 'RNFC':
                paramsext = ('Prefijo', 'RNC_id', 'RNCname')
                carr = 'RNC'
                namtoinx = 'RNCname'
            elif line == 'LNBTS':
                paramsext = ('Prefijo', 'LNBTSname')
                carr = 'LNBTS'
                namtoinx = 'LNBTSname'
            else:   # add columns to include in table query
                paramsext = ('Prefijo', 'LNBTS_id', 'earfcnDL', 'LNCELname', 'Banda')
                carr = carrierl(i)  # carrier number
                cart = carrtexl(i)
            paramst1.extend(paramsext)
            parstring = ','.join(paramst1)
            tabsq = tabconv(line)  # select reference table to get info
            try: # include queries for all and carrier, pending
                if line == 'LNBTS' or line == 'RNFC' or line == 'WBTS':
                    df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                                           index_col=[namtoinx, 'Prefijo'])
                else:  # 11 carrier related tables
                    if carr == 'all':
                        df = pd.read_sql_query("select " + parstring + " from " + tabsq + ";", conn,
                                               index_col=[namtoinx, 'Prefijo'])
                    else:
                        df = pd.read_sql_query(
                            "select " + parstring + " from " + tabsq + " where (" + str(carrfilt) + " = " + str(carr) + ");",
                                               conn, index_col=[namtoinx, 'Prefijo'])
                    df = df.dropna(subset=['Banda'])  # drop rows with band nan REVIEW IF NECESSARY
                print(df) # continue to process
                stpref = statzon(df)  # stats per parameter and prefijo
                st = par_audit(df)  # stats per parameter full set
                output = 'parametros.csv'
                st.to_csv(dat_dir / output)
                pyexcelerate_to_excel(wb, st, sheet_name=str(carr), index=True)
                df, st = cleaniparm2(df, st)  # standardized params and NaN>0.15*n removal
                st['topdisc'] = range(len(st))  # top disc counter by IQR-CV
                st['topdisc'] = st['topdisc'].floordiv(10)  # split disc in groups by 10
                st.sort_values(by=['Median'], inplace=True, ascending=[False])  # for better visualization
                st['counter'] = range(len(st))  # counter controls number of boxplots
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
                pngname = str(carr) + ".png"  # saveplot
                pngfile = dat_dir / pngname
                my_plot.save(pngfile, width=20, height=10, dpi=300)
                pnglist.append(pngfile)  # plots to be printed in pdf
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
                    pngname = str(carr) + str(j + 1) + ".png"
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


validatab('C:/SQLite', '20200522_sqlite.db', 'findtable', 'tabcustom')
customparam('C:/SQLite', '20200522_sqlite.db', 'tab_par')
