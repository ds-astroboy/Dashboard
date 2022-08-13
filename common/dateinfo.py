
from datetime import date, timedelta
# date.today().replace(day=1) - timedelta(days=1)
# date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
last_day_of_prev_month = '2022-05-31'
start_day_of_prev_month = '2022-05-01'
date_today = date.today()