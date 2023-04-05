import pygsheets
import emoji
import unicodedata
import pandas as pd
import yaml

# authorization
gc = pygsheets.authorize(service_file='your-service-file.json')

# Open spreadsheet and then worksheet
sh = gc.open_by_url('your-google-sheet-url')

wks_list = sh.worksheets()

for wks in wks_list:
    yamlData = []
    wks_title = wks.title
    if wks_title == '心情':
        continue
    data = wks.get_as_df()

    for index, row in data.iterrows():
        theRow = {
            'artist': str(row[0]).strip(),
            'music': str(row[1]).strip(),
            'allName': row[2].strip(),
            'url': row[3].strip()
        }
        yamlData.append(theRow)

    with open(f'playlist/{wks_title}.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(yamlData, file, allow_unicode=True)






