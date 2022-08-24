import re
from datetime import datetime
from dateutil.parser import parse

text_date = "Будет готово: понедельник 8 августа"

day, date = re.search("(?<=Будет готово: )(\w+)(.*)", text_date).groups()
# date = type(date)
date = date[1:]
print(day)
date = parse(date)
print(date)
