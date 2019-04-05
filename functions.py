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

def bart_image():
    a = ['https://i.imgur.com/KG9qUYb.png','https://i.imgur.com/WxUtb6T.jpg','https://i.imgur.com/NhprtjJ.jpg','https://i.imgur.com/pXilsu7.jpg','https://i.imgur.com/dYiYiFm.jpg','https://i.imgur.com/uY4M6Mx.jpg','https://i.imgur.com/nuKoOZk.png','https://i.imgur.com/QF70JM8.jpg','https://i.imgur.com/PCmXj8t.jpg','https://i.imgur.com/xVBs8cX.jpg','https://i.imgur.com/FNbeATG.jpg','https://i.imgur.com/Z4ufOZH.jpg','https://i.imgur.com/N385AB7.jpg','https://i.imgur.com/ErvBDk9.jpg','https://i.imgur.com/jeEXih2.jpg','https://i.imgur.com/uc1bBt8.png','https://i.imgur.com/CDB5D4Q.png','https://i.imgur.com/fXkke9G.jpg','https://i.imgur.com/kjqo2gN.jpg','https://i.imgur.com/MAdxt28.jpg','https://i.imgur.com/7l0Ai4T.jpg','https://i.imgur.com/qX4x2aD.jpg','https://i.imgur.com/elzhjLZ.jpg','https://i.imgur.com/vy7GtkY.png','https://i.imgur.com/dWwG2Uk.png','https://i.imgur.com/550oh1c.jpg','https://i.imgur.com/i4TEYNr.jpg','https://i.imgur.com/xijNZRu.jpg','https://i.imgur.com/Y9vOacY.jpg','https://i.imgur.com/yAFC7y6.png','https://i.imgur.com/1MAw2SD.png','https://i.imgur.com/9cMaTmS.jpg','https://i.imgur.com/GwqLVE7.jpg','https://i.imgur.com/ql3td93.jpg','https://i.imgur.com/hy1HLhj.jpg','https://i.imgur.com/VZMxKMk.jpg','https://i.imgur.com/dR1oFsw.jpg','https://i.imgur.com/Z9sz3oJ.jpg','https://i.imgur.com/8oqNp8h.jpg','https://i.imgur.com/GSrSjKj.jpg','https://i.imgur.com/frz0Av5.jpg','https://i.imgur.com/Ctk2owR.jpg','https://i.imgur.com/1Zld9zy.jpg','https://i.imgur.com/rogLdLS.jpg','https://i.imgur.com/cSL9Awz.jpg','https://i.imgur.com/MDO2UwT.jpg','https://i.imgur.com/b42QDdi.jpg','https://i.imgur.com/hCkiHme.png','https://i.imgur.com/P6jrhO6.png','https://i.imgur.com/oHVLwQG.png','https://i.imgur.com/ExY0mb9.png','https://i.imgur.com/Odb8VTK.png','https://i.imgur.com/2nLE8Aa.png','https://i.imgur.com/zlu2371.png','https://i.imgur.com/eH6avqy.png','https://i.imgur.com/vKJ5Jif.png','https://i.imgur.com/g5Le5rK.png','https://i.imgur.com/TKCaAzR.png','https://i.imgur.com/qWcvWLQ.png','https://i.imgur.com/xq8w053.png','https://i.imgur.com/vClvm18.png','https://i.imgur.com/DQAziIi.png','https://i.imgur.com/1RXNvS7.png','https://i.imgur.com/ib1e3f3.png','https://i.imgur.com/DG0tJVx.jpg','https://i.imgur.com/ovTSOfX.jpg','https://i.imgur.com/YzSH3rI.png','https://i.imgur.com/lpr9nbT.jpg','https://i.imgur.com/BUp4xNj.jpg','https://i.imgur.com/QVNAiz5.jpg','https://i.imgur.com/zee3vTs.jpg','https://i.imgur.com/Z6jQq4G.jpg','https://i.imgur.com/yVI6beX.jpg','https://i.imgur.com/cmLarXA.jpg','https://i.imgur.com/U9F7j9f.jpg','https://i.imgur.com/2bjkZe0.jpg','https://i.imgur.com/21fGrWZ.jpg','https://i.imgur.com/jlSWrSl.jpg','https://i.imgur.com/GMfVRic.jpg','https://i.imgur.com/zraoFoD.jpg','https://i.imgur.com/0cuwASi.jpg','https://i.imgur.com/0HUsG7K.jpg','https://i.imgur.com/DrRZ87g.jpg','https://i.imgur.com/jP2LbJl.jpg','https://i.imgur.com/RGqjy9b.jpg','https://i.imgur.com/6918pkd.jpg','https://i.imgur.com/TeaU24j.jpg','https://i.imgur.com/G2vg77A.jpg','https://i.imgur.com/Kzze4Lf.jpg','https://i.imgur.com/UgVeCrN.jpg','https://i.imgur.com/TvsEdkG.jpg','https://i.imgur.com/05QmS3w.jpg','https://i.imgur.com/HgxVnyT.jpg','https://i.imgur.com/JjgFOKk.jpg','https://i.imgur.com/EPKSrod.jpg','https://i.imgur.com/7ehcrt6.jpg','https://i.imgur.com/1U6GHUW.jpg','https://i.imgur.com/MKATl6d.jpg','https://i.imgur.com/q9RlBek.jpg','https://i.imgur.com/fTviVXd.jpg','https://i.imgur.com/2csk6ni.jpg','https://i.imgur.com/LOmYAFe.jpg','https://i.imgur.com/G0JRlcM.jpg','https://i.imgur.com/UuotaSZ.jpg','https://i.imgur.com/5xyw7dm.jpg','https://i.imgur.com/KOXUDbH.jpg']

    random.shuffle(a)

    return a[0]

def random_team():
    a = ["Atlanta Braves","Miami Marlins","New York Mets","Philadelphia Phillies","Washington Nationals","Chicago Cubs","Cincinnati Reds","Milwaukee Brewers","Pittsburgh Pirates","St.Louis Cardinals","Arizona Diamondbacks","Colorado Rockies","Los Angeles Dodgers","San Diego Padres","San Francisco Giants","Baltimore Orioles","Boston Red Sox","New York Yankees","Tampa Bay Rays","Toronto Blue Jays","Chicago White Sox","Cleveland Indians","Detroit Tigers","Kansas City Royals","Minnesota Twins","Houston Astros","Los Angeles Angels","Oakland Athletics","Seattle Mariners","Texas Rangers"]

    return a[hash(str(date)) % len(a)]
