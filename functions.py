from datetime import datetime
from pytz import timezone

def to_time(utc_time):
    ratime = timezone('America/Chicago')
    localtime = utc_time.astimezone(ratime)
    return localtime.strftime('%b %d %H:%M')1
