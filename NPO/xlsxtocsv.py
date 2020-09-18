import pandas as pd
from pathlib import Path
from rfpack.get_sheet_detailsc import get_sheet_details
from rfpack.csvfrmxlsxc import csvfrmxlsx


wrkfl = 'C:/xlsx/my.xlsx'  # path get with
xls_file = Path(wrkfl)
sheetsdic = get_sheet_details(xls_file)  # dictionary with sheet names and ids without opening xlsx file
df = pd.DataFrame.from_dict(sheetsdic)
csvfrmxlsx(xls_file, df)  # df with sheets to be converted
