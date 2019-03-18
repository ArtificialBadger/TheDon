from pytz import timezone
from datetime import datetime, time
from dateutil import tz, parser

def to_time(utc_time):
    ratime = timezone('America/Chicago')
    localtime = utc_time.astimezone(ratime)
    return localtime.strftime('%b %d %H:%M')

def from_time(ra_time):
    #ratime = timezone('America/Chicago')
    utctimezone = timezone('Etc/Greenwich')
    utctime = ra_time.astimezone(utctimezone)
    return utctime.strftime('%b %d %H:%M')

def my_parser(*args, default_tzinfo=tz.gettz("America/Chicago"), **kwargs):
    dt = parser.parse(*args, **kwargs)
    return dt.replace(tzinfo=dt.tzinfo or default_tzinfo)
