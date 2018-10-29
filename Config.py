from enum import Enum

class CancelOptions(Enum):
    EVERYONE = 1
    NONE = 2
    MODS = 3
    WHITELIST = 4

modlist = []
whitelist = []
app_secret = ""
currency = "RA Bucks"
currency_code = "RAB"
starting_amount = 100
allow_cancels = CancelOptions.MODS
allow_purges = False

