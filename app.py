import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)
print("Last Updated at : ",
      datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
