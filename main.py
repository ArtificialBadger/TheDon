#!/usr/bin/python3.6
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from tinydb import TinyDB, Query, where
from discord.utils import get
from tinydb.operations import delete
import random
import re

class User:
    def __init__(self, name, money):
        self.name = name
        self.money = money

class Bet:
    def __init__(self, user, line, bet, wager):
        self.user = user
        self.line = line
        self.bet = bet
        self.wager = wager

class Line:
    def __init__(self, host, line, description="", locked=False):
        self.host = host
        self.line = line
        self.description = description
        self.locked = locked


modlist = []
whitelist = []
app_secret = "NDg5NjE1NDkxMDc4MjkxNDU2.DntX6w.CHJnrwoNLpm971p5kkgBkESifRs"

bot = commands.Bot(command_prefix='$')

users = TinyDB('users.json')
bets = TinyDB('bets.json')
lines = TinyDB('lines.json')

pastBets = TinyDB('pastBets.json')
pastLines = TinyDB('pastLines.json')

query = Query()

@bot.event
async def on_ready():
    print("ready")

@bot.command(pass_context=True)
async def ImALittleBitch(ctx):
    accounts = users.search(query.name == str(ctx.message.author))
    if len(accounts) > 0:
        await bot.say("You already have an account you dumbo")
    else:
        users.insert(vars(User(str(ctx.message.author), 100)))
        await bot.say("{0} has been given 100 RABucks".format(str(ctx.message.author)))

@bot.command(pass_context=True)
async def leaderboard(ctx):
    orderedUsers = []
    for user in users.all():
        orderedUsers.append(User(user['name'], user['money']))
    orderedUsers = sorted(orderedUsers, key=lambda u: u.money)
    orderedUsers.reverse()
    embed = discord.Embed(title="Leaderboard", description="Users ranked by money", color=0xffffff)
    for user2 in orderedUsers:
        embed.add_field(name=user2.name, value=user2.money)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def money(ctx):
    user = users.get(query.name == str(ctx.message.author))
    if user is not None:
        await bot.say("You have {} RABucks".format(user['money']))

@bot.command(pass_context=True)
async def purgeAll(ctx):
    if (str(ctx.message.author) in modlist):
        users.purge()
        await bot.say("Users Purged")
        bets.purge()
        await bot.say("Bets Purged")
        lines.purge()
        await bot.say("Lines Purged")
    else:
        await bot.say("You are not authorized to purge")

@bot.command(pass_context=True)
async def purge(ctx, table):
    if (str(ctx.message.author) in modlist):
        if (table == "users"):
            users.purge()
            await bot.say("Users Purged")
        elif table == "bets":
            bets.purge()
            await bot.say("Bets Purged")
        elif table == "lines":
            lines.purge()
            await bot.say("Lines Purged")
        else:
            await bot.say("That's not something purgable you idiot")
    else:
        emoji = get(bot.get_all_emojis(), name='nou')
        await bot.say(emoji)

async def houseLine(ctx, line, *, description):
    activeLine = lines.get(query.line.matches('^' + line + '$', flags=re.IGNORECASE))

    if not activeLine is None:
        await bot.say("Line cannot be opened. There is already an open line with the same name.")
    elif str(ctx.message.author) in whitelist:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 10)}, query.name == "House")

        dbLine = Line("House", line, description)
        lines.insert(vars(dbLine))
        embed = discord.Embed(title="Line Opened", description="A new House Line has been opened", color=0xffffff)
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Author", value="House")
        embed.add_field(name="Description", value=description)
        await bot.say(embed=embed)
    else:
        await bot.say("Only trusted users can open a House Line")

@bot.command(pass_context=True)
async def house(ctx, line, *, description):
    await houseLine(ctx, line, description=description)

@bot.command(pass_context=True, name="BurtReynolds")
async def drive(ctx, *, description):
    await houseLine(ctx, "Drive", description=description)

@bot.command(pass_context=True)
async def unlock(ctx, line):
    hostLine = lines.get(query.line.matches(line, flags=re.IGNORECASE))
    host = hostLine['host']

    canUnlock = False

    if str(ctx.message.author) in modlist:
        canUnlock = True

    if (str(ctx.message.author) in whitelist) and (host == "House"):
        canUnlock = True

    if host == str(ctx.message.author):
        canUnlock = True

    if not hostLine['locked']:
        await bot.say("{} is already unlocked".format(line))
    elif canUnlock:
        lines.update({'locked': False}, query.line.matches('^' + line + '$', flags=re.IGNORECASE))
        await bot.say("Betting for {} has been unlocked, feel free to place bets".format(line))

    else:
        await bot.say("You cannot unlock a line you did not open")


async def lockLine(ctx, line):
    hostLine = lines.get(query.line.matches('^' + line + '$', flags=re.IGNORECASE))

    if hostLine is None:
        await bot.say("{} is not an open line".format(line))
        return

    host = hostLine['host']

    canLock = False

    if str(ctx.message.author) in modlist:
        canLock = True

    if str(ctx.message.author) in whitelist and host == 'House':
        canLock = True

    if host == str(ctx.message.author):
        canLock = True

    if hostLine['locked']:
        await bot.say("{} is already locked".format(hostLine['line']))
    elif canLock:
        lines.update({'locked': True}, query.line.matches('^' + line + '$', flags=re.IGNORECASE))
        await bot.say("Betting for {} has been locked. No more bets can be placed unless the line is unlocked".format(hostLine['line']))
    else:
        await bot.say("You cannot lock a line you did not open")


@bot.command(pass_context=True)
async def lock(ctx, line):
    await lockLine(ctx, line)

@bot.command(pass_context=True,name="o/u")
async def ou(ctx, line, *, description):
    activeLine = lines.get(query.line.matches('^' + line + '$', flags=re.IGNORECASE))

    if not activeLine is None:
        await bot.say("Line cannot be opened. There is already an open line with the same name.")
    else:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 5)}, query.name == "House")

        dbLine = Line(str(ctx.message.author), line, description, False)
        lines.insert(vars(dbLine))
        embed = discord.Embed(title="Line Opened", description="A new line has been opened", color=0xffffff)
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Author", value=str(ctx.message.author))
        embed.add_field(name="Description", value=description)
        await bot.say(embed=embed)

async def resolveLine(ctx, bet, result, owner, *, description=""):
    embed = discord.Embed(title="Line Resolved", description="description", color=0xffffff)

    winners = bets.search((query.bet == result) & (query.line.matches('^' + bet + '$', flags=re.IGNORECASE)))
    losers = bets.search((query.bet != result) & (query.line.matches('^' + bet + '$', flags=re.IGNORECASE)))
    lostMoney = 0
    wonMoney = 0

    winnersText = ""
    losersText = ""

    for winner in winners:
        user = users.get(query.name == winner.get('user'))
        newMoney = (user['money'] + int(winner.get('wager')))
        users.update({'money': newMoney}, query.name == user['name'])
        winnersText += "{0} has won {1} RABucks\r\n".format(winner['user'], int(winner.get('wager')))
        wonMoney += int(winner['wager'])

    if len(winners) > 0:
        embed.add_field(name="Winners", value=winnersText)
        embed.add_field(name="Total Money Won", value=wonMoney)
    else:
        embed.add_field(name="Winners", value="No Winners :(")

    for loser in losers:
        user = users.get(query.name == loser.get('user'))
        newMoney = (user['money'] - int(loser.get('wager')))
        users.update({'money': newMoney}, query.name == user['name'])
        losersText += "{0} has lost {1} RABucks\r\n".format(loser['user'], int(loser.get('wager')))
        lostMoney += int(loser['wager'])

    if len(losers) > 0:
        embed.add_field(name="Losers", value=losersText)
        embed.add_field(name="Total Money Lost", value=lostMoney)
    else:
        embed.add_field(name="Losers", value="No Losers!")


    if len(winners) == 0 and len(losers) == 0:
        await bot.say("There were no bets made on this line :(")

    houseMoney = int(lostMoney*.7)
    houseMoney -= int(wonMoney)
    moneyForLineOpener = min(len(winners), len(losers)) * 2
    moneyForLineOpener += int((lostMoney*.3))
    lineOpener = users.get(query.name == owner['host'])
    house = users.get(query.name == "House")
    if lineOpener is not None:
        newCash = lineOpener['money'] + moneyForLineOpener
        embed.add_field(name="Host", value="For hosting, {0} has been awarded {1} RABucks".format(owner['host'], moneyForLineOpener))
        users.update({'money': newCash}, query.name == owner['host'])

    if houseMoney > 0:
        embed.add_field(name="House", value="The house has gained {0} RABucks".format(houseMoney))
    else:
        embed.add_field(name="House", value="The house has lost {0} RABucks".format(0 - houseMoney))

    users.update({'money': (house['money'] + houseMoney)}, query.name == "House")
    bets.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))
    lines.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))

    #pastBets.insert(bet)

    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def resolve(ctx, bet, result=""):
    await resolveFunc(ctx, bet, result)

@bot.command(pass_context=True)
async def wash(ctx, bet):
    await resolveFunc(ctx, bet, "wash")

async def resolveFunc(ctx, bet, result=""):
    owner = lines.get(query.line.matches('^' + bet + '$', re.IGNORECASE))

    if (owner is None):
        await bot.say("{} is not an open line".format(bet))
    elif owner['host'] == "House":
        if str(ctx.message.author) in whitelist:
            if result == "wash":
                await bot.say("{} was a wash, everyone gets their money back!".format(owner['line']))
                bets.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))
                lines.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))
            elif result == "over" or result == "under":
                await resolveLine(ctx, bet, result, owner)
            else:
                await bot.say("Result must either be \"over\", \"under\" or \"wash\"")
        else:
            await bot.say("You are not authorized to resolve House Lines")
    elif str(ctx.message.author) != owner['host'] and not str(ctx.message.author) in modlist:
        await bot.say("You cannot close a line you did not open")
    elif result != "over" and result != "under" and result != "wash":
        await bot.say("Result must either be \"over\", \"under\" or \"wash\"")
    elif result == "wash":
        await bot.say("{} was a wash, everyone gets their money back!".format(owner['line']))
        bets.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))
        lines.remove(where('line').matches('^' + bet + '$', re.IGNORECASE))
    else:
        await resolveLine(ctx, bet, result, owner)

@bot.command(pass_context=True, name="myBets")
async def myBets1(ctx):
    await myBetsFunc(ctx)

@bot.command(pass_context=True, name="mybets")
async def myBets2(ctx):
    await myBetsFunc(ctx)

async def myBetsFunc(ctx):
    userOvers = bets.search((query.user == str(ctx.message.author)) & (query.bet == "over"))
    userUnders = bets.search((query.user == str(ctx.message.author)) & (query.bet == "under"))

    embed = discord.Embed(title="Bets for {}".format(str(ctx.message.author)))

    overtext = ""
    undertext = ""

    for over in userOvers:
        overtext += "{0} on {1} \r\n".format(over['wager'], over['line'])

    for under in userUnders:
        undertext += "{0} on {1} \r\n".format(under['wager'], under['line'])

    if overtext != "":
        embed.add_field(name="Overs", value=overtext)

    if undertext != "":
        embed.add_field(name="Unders", value=undertext)

    await bot.say(embed=embed)

async def myLinesFunc(ctx):
    myBets = bets.search(query.user == str(ctx.message.author))
    myOwnedLines = lines.search(query.host == str(ctx.message.author))

    lockedLines = list(map(lambda x: x['line'].lower(), lines.search(query.locked == True)))
    myLines = list(map(lambda x: x['line'].lower(), myBets))
    ownedLines = list(map(lambda x: x['line'].lower(), myOwnedLines))
    allLines = list(map(lambda x: x['line'], lines.all()))

    notMyLines = []

    for line in allLines:
        if not line.lower() in myLines and not line.lower() in ownedLines and not line.lower() in lockedLines:
            notMyLines.append(line)

    lockedLines = list(map(lambda x: x['line'], lines.search(query.locked == True)))
    myLines = list(map(lambda x: x['line'], myBets))
    ownedLines = list(map(lambda x: x['line'], myOwnedLines))

    embed = discord.Embed(title="All Lines", desciption="Lines with and without bets", color=0xffffff)

    if len(ownedLines) > 0:
        embed.add_field(name="Lines you are hosting", value="\r\n ".join(ownedLines))

    if len(myLines) > 0:
        embed.add_field(name="Lines you have a bet on", value="\r\n ".join(myLines))

    if len(notMyLines) > 0:
        embed.add_field(name="Lines you do not have a bet on", value="\r\n ".join(notMyLines))

    if len(lockedLines) > 0:
        embed.add_field(name="Locked Lines", value="\r\n ".join(lockedLines))

    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def myLines(ctx):
    await myLinesFunc(ctx)

@bot.command(pass_context=True)
async def mylines(ctx):
    await myLinesFunc(ctx)

@bot.command(pass_context=True, name="lines")
async def linesFunc(ctx):
    openLines = lines.search(query.locked == False)
    lockedLines = lines.search(query.locked == True)

    formattedOpenLines = " \r\n".join(list(map(lambda x: x['line'], openLines)))
    formattedLockedLines = " \r\n".join(list(map(lambda x: x['line'], lockedLines)))

    embed = discord.Embed(title="Lines", description="All currently open and locked lines", color=0xffffff)
    embed.set_footer(text="On Wisconsin")
    embed.add_field(name="Open Lines", value=formattedOpenLines)
    embed.add_field(name="Locked Lines", value=formattedLockedLines)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def info(ctx, line):
    activeLine = lines.get(query.line.matches('^' + line + '$', re.IGNORECASE))

    if activeLine == None:
        await bot.say("{} is not an open line".format(line))
        return

    embed = discord.Embed(title=activeLine['line'], description=activeLine['description'], color=0xffffff)
    embed.set_author(name="Host: {0}".format(activeLine['host']))
    embed.add_field(name="Locked" , value = activeLine['locked'])
    overText = ""
    underText = ""
    for bet in bets.search(query.line.matches('^' + line + '$', re.IGNORECASE)):
        if bet['bet'] == 'over':
            overText += "{0} - {1} \r\n".format(bet['wager'], bet['user'])
        elif bet['bet'] == 'under':
            underText += "{0} - {1} \r\n".format(bet['wager'], bet['user'])

    if overText != "":
        embed.add_field(name="Overs", value=overText)

    if underText != "":
        embed.add_field(name="Unders", value=underText)

    await bot.say(embed=embed)


@bot.command(pass_context=True, name="bets")
async def betsFunc(ctx, user: discord.Member = None):
    embed = discord.Embed(title="Bets", description="All currently open bets", color=0xffffff)
    embed.set_footer(text="On Wisconsin")
    betsDic = {}

    if user is None:
        iteratableBets = bets.all()
    else:
        iteratableBets = bets.search(query.user == str(user))

    for bet in iteratableBets:
        if bet['line'] in betsDic:
            betsDic[bet['line']] += "{1} for {0} - {2} \r\n".format(bet['user'], bet['bet'], bet['wager'])
        else:
            betsDic[bet['line']] = "{1} for {0} - {2}\r\n".format(bet['user'], bet['bet'], bet['wager'])

    for key, value in betsDic.items():
        embed.add_field(name=key, value=value)

    await bot.say(embed=embed)

async def overunder(ctx, bet, amount, ou):
    line = lines.get(query.line.matches('^' + bet + '$', re.IGNORECASE))
    user = users.get(query.name == str(ctx.message.author))
    previousBets = bets.search((query.user == str(ctx.message.author)))

    if previousBets is not None and len(previousBets) > 0:
        for previousBet in previousBets:
            if previousBet['line'] == bet:
                await bot.say("You already have a previous bet on {}".format(bet))
                return

    if user is None:
        await bot.say("You are not registered")
    elif line is None:
        await bot.say("{} is not an open line".format(bet))
    elif str(ctx.message.author) == line['host']:
        await bot.say("You cannot bet on your own line")
    elif not amount.isdigit():
        await bot.say("Your bet must be a positive integer")
    elif int(amount) > 100:
        await bot.say("The max bet is 100 RABucks")
    elif line['locked']:
        await bot.say("The betting is locked for {}".format(line['line']))
    else:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 10)}, query.name == "House")

        dbBet = Bet(str(ctx.message.author), bet, ou, amount)
        bets.insert(vars(dbBet))
        if ou == 'over':
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0xff0000)
        elif ou == 'under':
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0x0000ff)
        else:
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0x00ff00)
        embed.add_field(name="Line", value=line['line'])
        embed.add_field(name="description", value=line['description'])
        embed.add_field(name="Position", value=ou)
        embed.add_field(name="Amount", value=amount)
        embed.set_footer(text="On Wisconsin")
        embed.set_author(name=line['host'])
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rand(ctx, amount="0"):

    if amount == "0":
        amount = str(random.randint(1,101))

    if amount == "a positive integer":
        await bot.say("I bet you think your pretty fuckin clever don't you? Fuck off ya cheeky twat.")
        return
    elif not amount.isdigit():
        await bot.say("Your bet must be a positive integer. Dumb Bitch")
        return
    elif int(amount) > 100:
        await bot.say("The max bet is 100 RABucks")
        return

    # not own
    # not already bet upon
    # not 1locked

    myBets = bets.search(query.user == str(ctx.message.author))
    myLines = list(map(lambda x: x['line'], myBets))
    allLines = list(map(lambda x: x['line'], lines.search((query.locked == False) & (query.host != str(ctx.message.author)))))

    notMyLines = []

    for line in allLines:
        if not line in myLines:
            notMyLines.append(line)

    if len(notMyLines) > 0:
        randomLine = random.choice(notMyLines)
        randomPosition = random.choice(["over", "under"])
        await overunder(ctx, randomLine, amount, randomPosition)
    else:
        await bot.say("There are no eligible lines for you to bet on")


@bot.command(pass_context=True)
async def over(ctx, bet, amount):
    await overunder(ctx, bet, amount, "over")

@bot.command(pass_context=True)
async def under(ctx, bet, amount):
    await overunder(ctx, bet, amount, "under")

@bot.command(pass_context=True)
async def nou(ctx, user: discord.Member = None):
    if (user is None):
        emoji = get(bot.get_all_emojis(), name='nou')
        await bot.say(emoji)
    elif (str(ctx.message.author) == "pollytheparrot#4919"):
        await bot.say("This is not for you Polly")
    elif (str(ctx.message.author) in modlist):
        emoji = get(bot.get_all_emojis(), name='nou')
        await bot.say("{0} {1}".format(user.mention, emoji))
    elif (str(user) in modlist):
        await bot.say("**I WILL NOT TURN ON MY MASTER**")
    elif (str(ctx.message.author) == str(user)):
        await bot.say("Fuck off")
    else:
        await bot.say("{} No u".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def pinksock(ctx):
    emoji = get(bot.get_all_emojis(), name='pinksock')
    await bot.say(emoji)

bot.run(app_secret)

