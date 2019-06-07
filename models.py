class User:
    def __init__(self, name, money):
        self.name = name
        self.money = money

class Bet:
    def __init__(self, user, line, bet, wager, time):
        self.user = user
        self.line = line
        self.bet = bet
        self.wager = wager
        self.time = time

class Line:
    def __init__(self, host, line, description="", locked=False, locktime=None):
        self.host = host
        self.line = line
        self.description = description
        self.locked = locked
        self.locktime = locktime

class HistoricalBet:
    def __init__(self, user, line, position, wager, won, timePlaced, timeResolved):
        self.user = user
        self.line = line
        self.position = position
        self.wager = wager
        self.won = won
        self.timePlaced = timePlaced
        self.timeResolved = timeResolved

class HistoricalLine:
    def __init__(self, host, line, resolution, description, timeResolved):
        self.host = host
        self.line = line
        self.resolution = resolution
        self.description = description
        self.timeResolved = timeResolved

class Meme:
    def __init__(self, creator, name, link):
        self.creator = creator
        self.name = name
        self.link = link

class Answer:
    def __init__(self, response):
        self.response = response
