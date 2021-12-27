import pandas as pd
from csv_ical import Convert


convert = Convert()
convert.CSV_FILE_LOCATION = 'test44.csv'
convert.SAVE_LOCATION = 'calendar_219651.ics'


convert.read_ical(convert.SAVE_LOCATION)
convert.make_csv()
convert.save_csv(convert.CSV_FILE_LOCATION)




df = pd.read_csv('test.csv')