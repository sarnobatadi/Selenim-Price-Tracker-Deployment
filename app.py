import pytz
from datetime import datetime as dt
import datetime
IST = pytz.timezone('Asia/Kolkata')
datetime_ist = dt.now(IST)
print("Last Updated at : ",datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
current_time = datetime.datetime.now()
todaysDate = current_time.year*10000 + current_time.month*100 + current_time.day
print(todaysDate)
