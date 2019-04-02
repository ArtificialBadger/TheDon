from pytz import timezone
from datetime import date, datetime, time
from dateutil import tz, parser
import random

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


def random_team():
    random.seed(str(date.today()))

    a = ["Atlanta Braves","Miami Marlins","New York Mets","Philadelphia Phillies","Washington Nationals","Chicago Cubs","Cincinnati Reds","Milwaukee Brewers","Pittsburgh Pirates","St.Louis Cardinals","Arizona Diamondbacks","Colorado Rockies","Los Angeles Dodgers","San Diego Padres","San Francisco Giants","Baltimore Orioles","Boston Red Sox","New York Yankees","Tampa Bay Rays","Toronto Blue Jays","Chicago White Sox","Cleveland Indians","Detroit Tigers","Kansas City Royals","Minnesota Twins","Houston Astros","Los Angeles Angels","Oakland Athletics","Seattle Mariners","Texas Rangers"]

    random.shuffle(a)

    return a[0]
