from datetime import date
from pathlib import Path
from rfpack.validatabc import validatab
from rfpack.customparamc import customparam
from rfpack.pntopdc import pntopd
from rfpack.get_sheet_detailsc import get_sheet_details
from rfpack.get_sheetid_bynamec import *
from rfpack.csvfrmxlsxc import csvfrmxlsx
from rfpack.graffullc import graffull


# from pathlib import Path
# import pandas as pd
# from plotnine import *
# from rfpack.switcherc import znfrmt


# def graffull(xls_file, df, n):
#     pnglist1 = []
#     file = xls_file.parent / 'csv' / Path(df.loc[0][0] + '.csv')  # file Total
#     df1 = pd.read_csv(file)
#     for j in range(0, n):  # n plots, 3 regions per plot
#         smrzd = df1.loc[df1['prorder'] == j]  # filter info for zones set to be printed
#         custom_axis = theme(axis_text_x=element_text(color="grey", size=10, angle=90, hjust=.3),
#                             axis_text_y=element_text(color="grey", size=10),
#                             plot_title=element_text(size=25, face="bold"),
#                             axis_title=element_text(size=10),
#                             panel_spacing_x=1.6, panel_spacing_y=.45,  # review
#                             figure_size=(3 * 4, 5 * 4)
#                             )
#         smrzd_plot = (ggplot(data=smrzd, mapping=aes(x='parameter'))














#                       )
#         pngname = 'sumrzd' + str(j + 1) + '.png'
#         pngfile = xls_file.parent / pngname
#         smrzd_plot.save(pngfile, width=20, height=10, dpi=300)
#         pnglist1.append(pngfile)
#     return pnglist1


datab = Path('C:/SQLite/20200522_sqlite.db')
pdf_file = date.today().strftime("get_ipython().run_line_magic("y%m%d")", " + '_Feat1ParAudit.pdf'")
pdf_path = datab.parent / pdf_file
xls_file = Path(pdf_path.with_suffix('.xlsx'))
validatab(datab, 'findtable', 'tabcustom')
pnglist = customparam(datab, 'tab_par')  # generates png files and create xlsx file
rffl = 'C:/SQLite/tablasSQL.csv'  # sheets to select in xlsxsheets column
rfflph = Path(rffl)
clmntp = 'xlsxsheets'  # column to process
sheetsdic = get_sheet_details(xls_file)  # get sheet names and ids without opening xlsx file
df = get_sheetid_bynamef(rfflph, clmntp, sheetsdic)  # xlsxsheets column from csv table file
csvfrmxlsx(xls_file, df)  # df with sheets to be converted
pnglist1 = graffull(xls_file, df, 4)  # print Total info in 4 pages, 3 regions per page
pnglist1.extend(pnglist) 
pntopd(pdf_path, pnglist1, 50, 550, 500, 500)












