import datetime

DAY = datetime.timedelta(1)
today = datetime.date.today()
date_list = []
for item in range(10):
    year = today.year
    month = today.month
    day = today.day
    date_list += [[year, month, day]]
    today = today + DAY

print(date_list)