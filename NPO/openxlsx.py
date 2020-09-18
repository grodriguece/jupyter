from pathlib import Path
import os
import xmltodict
import shutil
import zipfile


def get_sheet_details(filename):
    sheets = []
    # Make a temporary directory with the file name
    directory_to_extract_to = (filename.with_suffix(''))
    directory_to_extract_to.mkdir(parents=True, exist_ok=True)
    # Extract the xlsx file as it is just a zip file
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    # Open the workbook.xml which is very light and only has meta data, get sheets from it
    path_to_workbook = directory_to_extract_to / 'xl' / 'workbook.xml'
    with open(path_to_workbook, 'r') as f:
        xml = f.read()
        dictionary = xmltodict.parse(xml)
        for sheet in dictionary['workbook']['sheets']['sheet']:
            sheet_details = {
                'id': sheet['@sheetId'],  # can be sheetId for some versions
                'name': sheet['@name']  # can be name
            }
            sheets.append(sheet_details)
    # Delete the extracted files directory
    shutil.rmtree(directory_to_extract_to)
    return sheets  # with sheetid, it can be saved with xlsx2csv


xlsxfile = Path('C:/SQLite/200826_Feat1ParAudit - Copy.xlsx')
shets = get_sheet_details(xlsxfile)
print(shets)

# How to obtain sheet names from XLS files without loading the whole file?
