#!/usr/bin/python3.6
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from tinydb import TinyDB, Query, where
from discord.utils import get
from tinydb.operations import delete
import random
import functions
import re
import importlib
import Config
from dateutil import parser
from DateTimeSerializer import DateTimeSerializer
from datetime import datetime, date
from tinydb_serialization import Serializer, SerializationMiddleware
from pytz import timezone
import sys
import requests
import json
import uuid
from models import Line, User, Bet, HistoricalLine, HistoricalBet, Meme, Answer
from betting import Betting
from eightball import EightBall
from mimic import Mimic
sys.setrecursionlimit(100000)

instance_id = uuid.uuid1()

modlist = Config.modlist
whitelist = Config.whitelist
app_secret = Config.app_secret

bot = commands.Bot(command_prefix='$')
bot.add_cog(Betting(bot))
bot.add_cog(EightBall(bot))
bot.add_cog(Mimic(bot))

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

serialization2 = SerializationMiddleware()
serialization2.register_serializer(DateTimeSerializer(), 'TinyDate')

serialization3 = SerializationMiddleware()
serialization3.register_serializer(DateTimeSerializer(), 'TinyDate')

serialization4 = SerializationMiddleware()
serialization4.register_serializer(DateTimeSerializer(), 'TinyDate')

users = TinyDB('users.json')
bets = TinyDB('bets.json', storage=serialization)
lines = TinyDB('lines.json', storage=serialization2)

historical_bets = TinyDB('pastBets.json', storage=serialization3)
historical_lines = TinyDB('pastLines.json', storage=serialization4)

memes = TinyDB('memes.json')

last_error_count = 0
last_error_user = ''

query = Query()

@bot.event
async def on_ready():
    print("ready")
    #await bot.send_message(discord.Object(id='490306602545446932'), 'Up and running!')

#@bot.event
#async def on_command_error(ctx, error):
async def thing(ctx, error):
    global last_error_count
    global last_error_user

    author = str(ctx.message.author)

    if author == last_error_user:
        last_error_count += 1
    else:
        last_error_user = author
        last_error_count = 0

    if last_error_count == 2:
        await ctx.send("OK {0} you can fuck off now".format(ctx.message.author.mention))
    elif last_error_count == 3:
        await ctx.send("Don't make me get nasty")
    elif last_error_count == 4:
        await ctx.send("Do it one more time you rancid fuck")
    elif last_error_count == 5:
        await ctx.send("{0} has been added to the blacklist".format(ctx.message.author.mention))
    elif last_error_count > 5:
        await ctx.send("{0} has been docked 100 RAB".format(ctx.message.author.mention))
    else:
        await ctx.send("I have no fucking idea what you want me to do")

@bot.event
async def on_message(message):
    if not message.author.bot and "lamar" in message.content.lower():
        llamaString = message.content.replace('Lamar', 'Llama')
        newString = re.compile("lamar", re.IGNORECASE)
        print(message)
        await message.channel.send(newString.sub('llama', llamaString))

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def meme(ctx, meme_name, image_link):
    current_meme_list = memes.search(query.name == meme_name)
    if len(current_meme_list) > 0:
        await ctx.send("That is already a registered meme you Dumbo");
    else:
        memes.insert(vars(Meme(str(ctx.message.author), meme_name, image_link)))
        await ctx.send("Registered new meme!");

@bot.command(pass_context=True)
async def unmeme(ctx, meme_name):
    memes.remove(query.name == meme_name)
    await ctx.send("Killed the meme dream!")

@bot.command(pass_context=True)
async def allbart(ctx):
    meme_list = memes.all()
    embed = discord.Embed(title="Bart Memes", color=0x1a2b3c)
    memetext = len(meme_list)
    embed.add_field(name="Number of Bart Memes", value=memetext)
    await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases = ["imalittlebitch", "IAmALittleBitch", "iamalittlebitch"], brief="Sets a user up with {0} {1}".format(Config.starting_amount, Config.currency_code), description="Initializes a user with {0} {1} and allows them to begin placing bets. All users need to call this function before being able to place bets or open lines.".format(Config.starting_amount, Config.currency))
async def ImALittleBitch(ctx):
    accounts = users.search(query.name == str(ctx.message.author))
    if len(accounts) > 0:
        await ctx.send("You already have an account you dumbo")
    else:
        users.insert(vars(User(str(ctx.message.author), Config.starting_amount)))
        await ctx.send("{0} has been given {1} {2}".format(str(ctx.message.author), Config.starting_amount, Config.currency))

@bot.command(pass_context=True, brief="Shows the leaders in order of {0}".format(Config.currency), description="Displays a full ordering of users, ordered by {0}".format(Config.currency))
async def leaderboard(ctx):
    orderedUsers = []
    for user in users.all():
        orderedUsers.append(User(user['name'], user['money']))
    orderedUsers = sorted(orderedUsers, key=lambda u: u.money)
    orderedUsers.reverse()
    if len(orderedUsers) > 25:
        leaderboard_users = orderedUsers[0:21] + orderedUsers[-3:]
    else:
        leaderboard_users = orderedUsers

    embed = discord.Embed(title="Leaderboard", description="Users ranked by money", color=0xffffff)
    for user2 in leaderboard_users:
        embed.add_field(name=user2.name, value=user2.money)
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Shows the callers {0}".format(Config.currency), description="Shows the amount of {0} of the command invoker".format(Config.currency))
async def money(ctx):
    user = users.get(query.name == str(ctx.message.author))
    if user is not None:
        await ctx.send("You have {} RABucks".format(user['money']))

@bot.command(pass_context=True, brief="Gets a team for Box to cheer for", description="Gives a random team for Box to cheer for. Changes daily.")
async def boxwagon(ctx):
    await ctx.send(functions.random_team())

@bot.command(brief="heck", alias=['heck'])
async def dale(ctx):
    embed = discord.Embed(color=0xc0c0c0)
    embed.set_image(url='https://media.tenor.com/images/b650be0d3e46da3f24a771a3725cf360/tenor.gif')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Purges all the data", description="Very dangerous command\r\nOnly invokeable by mods with the allow_puges flag set to true")
async def purgeAll(ctx):
    if Config.allow_purges:
        if (str(ctx.message.author) in modlist):
            users.purge()
            await ctx.send("Users Purged")
            bets.purge()
            await ctx.send("Bets Purged")
            lines.purge()
            await ctx.send("Lines Purged")

        else:
            await ctx.send("You are not authorized to purge")
    else:
        await ctx.send("Purging is disallowed. Set the allow_purge flag to True to allow purging")

@bot.command(pass_context=True, brief="Purges specific tables", description="Purges either the historical data, users, bets, or lines")
async def purge(ctx, table):
    if Config.allow_purges:
        if (str(ctx.message.author) in modlist):
            if (table.lower() == "history"):
                historical_bets.purge()
                await ctx.send("Historical Lines and Bets Purged")
            elif (table.lower() == "users"):
                users.purge()
                await ctx.send("Users Purged")
            elif table.lower() == "bets":
                bets.purge()
                await ctx.send("Bets Purged")
            elif table.lower() == "lines":
                lines.purge()
                await ctx.send("Lines Purged")
            else:
                await ctx.send("That's not something purgable you idiot")
        else:
            await ctx.send("You are not authorized to purge")
    else:
        await ctx.send("Purging is disallowed. Set the allow_purge flag to True to allow purging")

@bot.command(pass_context=True, brief="lock time has to be something like 2019-03-18T20:00")
async def autolock(ctx, line, locktime):
    localtime = functions.my_parser(locktime)
    dt = parser.parse(functions.from_time(localtime))
    lines.update({'locktime': dt}, query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))
    await ctx.send(line + " has been autolocked at " + functions.to_time(dt))

async def houseLine(ctx, line, description, locktime = datetime.max):
    activeLine = lines.get(query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))

    if not activeLine is None:
        await ctx.send("Line cannot be opened. There is already an open line with the same name.")
    elif str(ctx.message.author) in whitelist:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 10)}, query.name == "House")

        dbLine = Line("House", line, description, False, locktime)
        lines.insert(vars(dbLine))
        embed = discord.Embed(title="Line Opened", description="A new House Line has been opened", color=0xffffff)
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Author", value="House")
        if not description == "":
            embed.add_field(name="Description", value=description)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Only trusted users can open a House Line")

@bot.command(pass_context=True, brief="Opens a house line", description="Opens a line with the House as an owner. Generally used for lines with pre-established odds, such as Spreads and Over Unders.")
async def house(ctx, line, *, description=""):
    await houseLine(ctx, line, description)

@bot.command(pass_context=True, name="BurtReynolds", brief="Opens a House line called Drive", description="Opens a house line called Drive. Created specifically for Dustin on his daily commutes.")
async def drive(ctx, *, description):
    await houseLine(ctx, "Drive", description)

@bot.command(pass_context=True)
async def croot(ctx, year, *, name):

    url = 'https://247sports.com/Season/{}-Football/Recruits.json?&Items=15&Page=1&Player.FullName={}'.format(year, name)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    search = requests.get(url=url, headers=headers)
    search = json.loads(search.text)
    if not search:
        await ctx.send('wut')
    elif len(search) > 1:
        searched = search[0]
    else:
        searched = search[0]

    player = search[0]['Player']
    full_name = player['FullName']
    position = player['PrimaryPlayerPosition']['Abbreviation']

    height = player['Height'].split('-')[1]
    if float(height).is_integer():
        inches = int(height)
    else:
        inches = height

    measurables = str(int(player['Height'].split('-')[0])) + 'ft ' + str(inches) + 'in\r\n' + str(int(player['Weight'])) + 'lbs' + '\r\n'

    #rankings = player['CompositeStarRating']
    rankings = ':star:' * int(player['CompositeStarRating'])
    rankings_body = '%.5f' % float(player['CompositeRating'])
    rankings_body += '\n#' + str(int(player['NationalRank'])) + ' Overall'
    rankings_body += '\n#' + str(int(player['PositionRank'])) + ' Position'
    rankings_body += '\n#' + str(int(player['StateRank'])) + ' State'

    a = player['PlayerHighSchool']['Name']
    b = player['Hometown']['City'] + ' ' + player['Hometown']['State']
    measurables += b

    embed = discord.Embed(title=full_name + ' - '+ player['PrimaryPlayerPosition']['Abbreviation'], desciption=position, color=0xffffff)

    if searched['CommitedInstitutionTeamImage'] is not None:
        embed.set_thumbnail(url = searched['CommitedInstitutionTeamImage'])
    else:
        embed.set_thumbnail(url = 'https://www.edmontoncorporatechallenge.com/Sports%20Icons/unknown-challenge.png')

    embed.set_image(url = player['DefaultAssetUrl'])

    embed.add_field(name=a, value=measurables)
    embed.add_field(value=rankings_body, name=rankings)

    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Unlocks a line", description="Unlocks a line to further betting. Only has an effect when the line is currently locked.")
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
        await ctx.send("{} is already unlocked".format(line))
    elif canUnlock:
        lines.update({'locked': False}, query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))
        await ctx.send("Betting for {} has been unlocked, feel free to place bets".format(line))

    else:
        await ctx.send("You cannot unlock a line you did not open")


async def lockLine(ctx, line):
    hostLine = lines.get(query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))

    if hostLine is None:
        await ctx.send("{} is not an open line".format(line))
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
        await ctx.send("{} is already locked".format(hostLine['line']))
    elif canLock:
        lines.update({'locked': True}, query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))
        await ctx.send("Betting for {} has been locked. No more bets can be placed unless the line is unlocked".format(hostLine['line']))
    else:
        await ctx.send("You cannot lock a line you did not open")


@bot.command(pass_context=True, brief="Locks a line", description="Locks a line so that no more bets can be made. Line must be unlocked for future betting to occur.")
async def lock(ctx, line):
    await lockLine(ctx, line)

@bot.command(pass_context=True,name="o/u", brief="Opens a line", description="Opens a line to betting. The first word following o/u will be the line name and all subsequent text will be used as the description of the line.")
async def ou(ctx, line, *, description):
    activeLine = lines.get(query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE))

    if not activeLine is None:
        await ctx.send("Line cannot be opened. There is already an open line with the same name.")
    else:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 10)}, query.name == "House")

        dbLine = Line(str(ctx.message.author), line, description, False)
        lines.insert(vars(dbLine))
        embed = discord.Embed(title="Line Opened", description="A new line has been opened", color=0xffffff)
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Author", value=str(ctx.message.author))
        embed.add_field(name="Description", value=description)
        await ctx.send(embed=embed)

async def resolveLine(ctx, line, result, owner, description=""):
    dbLine = lines.get(query.line.matches('^' + re.escape(line) + '$', re.IGNORECASE))
    if dbLine is None:
        await ctx.send("Something has gone terribly wrong. Error code NL100")

    embed = discord.Embed(title="Line Resolved - {0}".format(line), description=dbLine['description'], color=0xffffff)

    if not description == "":
        embed.add_field(name="Resolution Description", value=description)

    winners = bets.search((query.bet == result) & (query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE)))
    losers = bets.search((query.bet != result) & (query.line.matches('^' + re.escape(line) + '$', flags=re.IGNORECASE)))
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

        historical_bet = HistoricalBet(winner['user'], winner['line'], winner['bet'], winner['wager'], True, winner['time'], datetime.utcnow())
        historical_bets.insert(vars(historical_bet))

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

        historical_bet = HistoricalBet(loser['user'], loser['line'], loser['bet'], loser['wager'], False, loser['time'], datetime.utcnow())
        historical_bets.insert(vars(historical_bet))

    if len(losers) > 0:
        embed.add_field(name="Losers", value=losersText)
        embed.add_field(name="Total Money Lost", value=lostMoney)
    else:
        embed.add_field(name="Losers", value="No Losers!")


    if len(winners) == 0 and len(losers) == 0:
        await ctx.send("There were no bets made on this line :(")
    else:
        houseMoney = int(lostMoney*.7)
        houseMoney -= int(wonMoney)
        moneyForLineOpener = min(len(winners), len(losers)) * 5
        moneyForLineOpener += int((lostMoney*.3))
        lineOpener = users.get(query.name == owner['host'])
        house = users.get(query.name == "House")
        if lineOpener is not None:
            newCash = lineOpener['money'] + moneyForLineOpener
            embed.add_field(name="Host", value="For hosting, {0} has been awarded {1} RABucks".format(owner['host'], moneyForLineOpener))
            users.update({'money': newCash}, query.name == owner['host'])

        users.update({'money': (house['money'] + houseMoney)}, query.name == "House")

        if houseMoney > 0:
            embed.add_field(name="House", value="The house has gained {0} RABucks".format(houseMoney))
        else:
            embed.add_field(name="House", value="The house has lost {0} RABucks".format(0 - houseMoney))
        await ctx.send(embed=embed)

    bets.remove(where('line').matches('^' + re.escape(line) + '$', re.IGNORECASE))
    lines.remove(where('line').matches('^' + re.escape(line) + '$', re.IGNORECASE))

    historical_line = HistoricalLine(owner['host'], dbLine['line'], result, dbLine['description'], timeResolved = datetime.utcnow())
    historical_lines.insert(vars(historical_line))


@bot.command(pass_context=True, brief="Resolves an open line", description="Resolves an open line. Can be resolved either over, under, or wash.\r\nWinners are given an amount of {0} to their wager, losers are deducted an amount of {0} equal to their wager.\r\nMoney is granted to the line opener during resolution.\r\nNo money is given or taken in the case of a wash".format(Config.currency))
async def resolve(ctx, bet, result="", *, description=""):
    await resolveFunc(ctx, bet, result, description)

@bot.command(pass_context=True, brief="Washes a line", description="Resolves a line as a wash/push. No money is taken nor given.")
async def wash(ctx, bet):
    await resolveFunc(ctx, bet, "wash")

async def resolveFunc(ctx, bet, result="", description=""):
    owner = lines.get(query.line.matches('^' + re.escape(bet) + '$', re.IGNORECASE))

    if (owner is None):
        await ctx.send("{} is not an open line".format(bet))
    elif owner['host'] == "House":
        if str(ctx.message.author) in whitelist:
            if result == "wash":
                await ctx.send("{} was a wash, everyone gets their money back!".format(owner['line']))
                bets.remove(where('line').matches('^' + re.escape(bet) + '$', re.IGNORECASE))
                lines.remove(where('line').matches('^' + re.escape(bet) + '$', re.IGNORECASE))
            elif result == "over" or result == "under":
                await resolveLine(ctx, bet, result, owner, description)
            else:
                await ctx.send("Result must either be \"over\", \"under\" or \"wash\"")
        else:
            await ctx.send("You are not authorized to resolve House Lines")
    elif str(ctx.message.author) != owner['host'] and not str(ctx.message.author) in modlist:
        await ctx.send("You cannot close a line you did not open")
    elif result != "over" and result != "under" and result != "wash":
        await ctx.send("Result must either be \"over\", \"under\" or \"wash\"")
    elif result == "wash":
        await ctx.send("{} was a wash, everyone gets their money back!".format(owner['line']))
        bets.remove(where('line').matches('^' + re.escape(bet) + '$', re.IGNORECASE))
        lines.remove(where('line').matches('^' + re.escape(bet) + '$', re.IGNORECASE))
    else:
        await resolveLine(ctx, bet, result, owner, description)

@bot.command(pass_context=True, name="myBets", brief="Shows the callers active bets", description="Displays all the active bets bade by the command invoker.")
async def myBets1(ctx):
    await myBetsFunc(ctx)

@bot.command(pass_context=True, name="mybets", brief="Shows the callers active bets", description="Displays all the active bets bade by the command invoker.")
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

    await ctx.send(embed=embed)

def getlocktime(x):
    return x['locktime'] or datetime(year = 3000, month = 1, day = 1)

async def myLinesFunc(ctx):
    myBets = bets.search(query.user == str(ctx.message.author))
    myOwnedLines = lines.search(query.host == str(ctx.message.author))

    lockedLines = list(map(lambda x: x['line'].lower(), lines.search(query.locked == True)))
    myLines = list(map(lambda x: x['line'].lower(), myBets))
    ownedLines = list(map(lambda x: x['line'].lower(), myOwnedLines))
    allLines = list(
        map(lambda x: x['line'], sorted(lines.all(), key=getlocktime))
        )

    notMyLines = []

    for line in allLines:
        if not line.lower() in myLines and not line.lower() in ownedLines and not line.lower() in lockedLines:
            notMyLines.append(line)

    lockedLines = list(map(lambda x: x['line'], lines.search(query.locked == True)))
    myLines = list(map(lambda x: x['line'], myBets))
    ownedLines = list(map(lambda x: x['line'], myOwnedLines))

    embed = discord.Embed(title="All Lines", desciption="Lines with and without bets", color=0xffffff)

    if len(ownedLines) > 0:
        embed.add_field(name="Lines you are hosting", value="\r\n ".join(ownedLines[:25]))

    if len(myLines) > 0:
        embed.add_field(name="Lines you have a bet on", value="\r\n ".join(myLines[:25]))

    if len(notMyLines) > 0:
        embed.add_field(name="Lines you do not have a bet on", value="\r\n ".join(notMyLines[:25]))

    if len(lockedLines) > 0:
        embed.add_field(name="Locked Lines", value="\r\n ".join(lockedLines[:25]))

    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Shows all lines in relation to the caller", description="Shows all the lines that the command invoker is hosting, has bets on, and the locked and unlocked lines.")
async def myLines(ctx):
    await myLinesFunc(ctx)

@bot.command(pass_context=True, brief="Shows all lines in relation to the caller", description="Shows all the lines that the command invoker is hosting, has bets on, and the locked and unlocked lines.")
async def mylines(ctx):
    await myLinesFunc(ctx)

@bot.command(pass_context=True, name="lines", brief="Shows categorized lines", description="Shows all active lines, categorized into locked and unlocked lines.")
async def linesFunc(ctx):
    openLines = lines.search(query.locked == False)
    lockedLines = lines.search(query.locked == True)

    formattedOpenLines = " \r\n".join(list(map(lambda x: x['line'], openLines)))
    formattedLockedLines = " \r\n".join(list(map(lambda x: x['line'], lockedLines)))

    embed = discord.Embed(title="Lines", description="All currently open and locked lines", color=0xffffff)
    embed.add_field(name="Website", value="http://www.ragambling.info");
    embed.add_field(name="Open Lines", value=formattedOpenLines)
    embed.add_field(name="Locked Lines", value=formattedLockedLines)
    embed.set_footer(text="On Wisconsin")
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Gives info about a specific line", description="Gives all availible info about a line")
async def info(ctx, line):
    activeLine = lines.get(query.line.matches('^' + re.escape(line) + '$', re.IGNORECASE))

    if activeLine == None:
        await ctx.send("{} is not an open line".format(line))
        return

    embed = discord.Embed(title=activeLine['line'], description=activeLine['description'], color=0xffffff)
    embed.set_author(name="Host: {0}".format(activeLine['host']))
    if (activeLine['locked']):
        embed.add_field(name="Locked" , value = True)
    elif activeLine['locktime'] is not None and datetime.utcnow() > activeLine['locktime']:
        await lockLine(ctx, line)
        embed.add_field(name="Locked" , value = True)
    else:
        embed.add_field(name="Locked" , value = False)

    overText = ""
    underText = ""
    for bet in bets.search(query.line.matches('^' + re.escape(line) + '$', re.IGNORECASE)):
        if bet['bet'] == 'over':
            overText += "{0} - {1} \r\n".format(bet['wager'], bet['user'])
        elif bet['bet'] == 'under':
            underText += "{0} - {1} \r\n".format(bet['wager'], bet['user'])

    if overText != "":
        embed.add_field(name="Overs", value=overText)

    if underText != "":
        embed.add_field(name="Unders", value=underText)

    await ctx.send(embed=embed)


@bot.command(pass_context=True, brief="REMOVE THIS PLZ", description="")
async def historicalLines(ctx, user: discord.Member = None):
    embed = discord.Embed(title="Bets", description="All Previous Lines", color=0xffffff)
    embed.set_footer(text="On Wisconsin")

    historical_lines_text = ""

    ordered_lines = sorted(historical_lines.all(), key=lambda x: x['timeResolved'])
    ordered_lines.reverse()

    for historical_line in ordered_lines:
        historical_lines_text += "{0} resolved as {1} at {2}\r\n".format(historical_line['line'], historical_line['resolution'], functions.to_time(historical_line['timeResolved']))

    if historical_lines_text != "":
        embed.add_field(name="All Previous Lines", value=historical_lines_text)

    await ctx.send(embed=embed)


@bot.command(pass_context=True, brief="History for a user", description="")
async def history(ctx):
    embed = discord.Embed(title="Bets", description="Previous bets", color=0xffffff)
    embed.set_footer(text="On Wisconsin")

    historical_bets_text = ""

    ordered_bets = sorted(historical_bets.search(query.user == str(ctx.message.author)), key=lambda x: x['timeResolved'])
    ordered_bets.reverse()

    del ordered_bets[20:]

    for historical_bet in ordered_bets:
        if historical_bet['won']:
            historical_bets_text += "won {0} on {1} at {2}\r\n".format(historical_bet['wager'], historical_bet['line'], functions.to_time(historical_bet['timeResolved']))
        else:
            historical_bets_text += "lost {0} on {1} at {2}\r\n".format(historical_bet['wager'], historical_bet['line'], functions.to_time(historical_bet['timeResolved']))
    if historical_bets_text != "":
        embed.add_field(name="Most Recent Bets", value=historical_bets_text)


    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="REMOVE THIS PLZ", description="")
async def historicalBets(ctx, user: discord.Member = None):
    embed = discord.Embed(title="Bets", description="All Historical Bets (for testing purposes only)", color=0xffffff)
    embed.set_footer(text="On Wisconsin")

    historical_bets_text = ""

    ordered_bets = sorted(historical_bets.all(), key=lambda x: x['timePlaced'])
    ordered_bets.reverse()

    for historical_bet in ordered_bets:
        if historical_bet['won']:
            historical_bets_text += "{0} won {1} on {2} at {3}\r\n".format(historical_bet['user'], historical_bet['wager'], historical_bet['line'], functions.to_time(historical_bet['timePlaced']))
        else:
            historical_bets_text += "{0} lost {1} on {2} at {3}\r\n".format(historical_bet['user'], historical_bet['wager'], historical_bet['line'], functions.to_time(historical_bet['timePlaced']))

    if historical_bets_text != "":
        embed.add_field(name="All Previous Bets", value=historical_bets_text)

    await ctx.send(embed=embed)

@bot.command(pass_context=True, name="bets", brief="", description="")
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

    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def bounty(ctx, user: discord.Member, amount, *, description="finding a bug"):

    user = users.get(query.name == str(user))

    if not str(ctx.message.author) in modlist:
        await ctx.send("Only mods can award bounties")
    elif user is None:
        await ctx.send("User is not registered in the system")
    elif not amount.isdigit():
        await ctx.send("Bounty must be a positive integer")
    elif int(amount) > 1000:
        await ctx.send("Max bounty is 1000 RAB")
    else:
        users.update({'money': (user['money'] + int(amount))}, query.name == user['name'])
        await ctx.send("{0} has been awarded a bounty of {1} RA Bucks for {2}!".format(user['name'], int(amount), description))

@bot.command(pass_context=True, brief="", description="")
async def mint(ctx, amount):

    user = users.get(query.name == "House")

    if not str(ctx.message.author) in modlist:
        await ctx.send("Only mods can award bounties")
    elif not amount.isdigit():
        await ctx.send("Bounty must be a positive integer")
    elif int(amount) > 10000:
        await ctx.send("Max bounty is 10000 RAB")
    else:
        users.update({'money': (user['money'] + int(amount))}, query.name == user['name'])
        await ctx.send("{0} has printed {1} RA Bucks!".format(user['name'], int(amount)))


@bot.command(pass_context=True, brief="", description="")
async def adjust(ctx, user: discord.Member, amount):

    user = users.get(query.name == str(user))

    if not str(ctx.message.author) in modlist:
        await ctx.send("Only mods can adjust money")
    elif user is None:
        await ctx.send("User is not registered in the system")
    elif not is_integer(amount):
        await ctx.send("The entered number is not an integer")
    elif int(amount) > 2000 or int(amount) < -2000:
        await ctx.send("Maximum adjustment is -2000 to 2000 RAB")
    else:
        users.update({'money': (user['money'] + int(amount))}, query.name == user['name'])
        await ctx.send("{0} has had their money adjusted by {1} from {2} to {3}".format(user['name'], int(amount), user['money'], user['money'] + int(amount)))

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

async def overunder(ctx, userLine, amount, ou, silent = False):
    line = lines.get(query.line.matches('^' + re.escape(userLine) + '$', re.IGNORECASE))
    user = users.get(query.name == str(ctx.message.author))
    previousBets = bets.search((query.user == str(ctx.message.author)))

    if previousBets is not None and len(previousBets) > 0:
        for previousBet in previousBets:
            if previousBet['line'].lower() == userLine.lower():
                await ctx.send("You already have a previous bet on {}".format(userLine))
                return

    if user is None and not silent:
        await ctx.send(str(ctx.message.author))
        await ctx.send("You are not registered")
    elif line is None and not silent:
        await ctx.send("{} is not an open line".format(userLine))
    elif str(ctx.message.author) == line['host'] and not silent:
        await ctx.send("You cannot bet on your own line")
    elif not amount.isdigit() and not silent:
        await ctx.send("Your bet must be a positive integer")
    elif int(amount) > 1000 and not silent:
        await ctx.send("The max bet is 1000 RABucks")
    elif line['locked'] and not silent:
        await ctx.send("The betting is locked for {}".format(line['line']))
    elif line['locktime'] is not None and datetime.utcnow() > line['locktime'] and not silent:
        await lockLine(ctx, userLine)
    else:
        house = users.get(query.name == "House")
        users.update({'money': (house['money'] + 5)}, query.name == "House")

        dbBet = Bet(str(ctx.message.author), userLine, ou, amount, time=datetime.utcnow())
        bets.insert(vars(dbBet))
        if ou == 'over':
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0xff0000)
        elif ou == 'under':
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0x0000ff)
        else:
            embed = discord.Embed(title="Bet Made", description="Bet made by {}".format(ctx.message.author), color=0x00ff00)
        embed.add_field(name="Line", value=line['line'])
        if not line['description'] == "":
            embed.add_field(name="description", value=line['description'])

        embed.add_field(name="Position", value=ou)
        embed.add_field(name="Amount", value=amount)
        embed.add_field(name="Time Placed (RA Time)", value=functions.to_time(dbBet.time))
        embed.set_footer(text="On Wisconsin")
        embed.set_author(name=line['host'])
        if not silent:
            await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def cancel(ctx, userLine=""):

    can_cancel = False

    #TODO Rest of configs for can_cancel

    if Config.allow_cancels == Config.CancelOptions.MODS and str(ctx.message.author) in modlist:
        can_cancel = True
    else:
        can_cancel = False

    if can_cancel:
        line = lines.get(query.line.matches('^' + re.escape(userLine) + '$', re.IGNORECASE))
        user = users.get(query.name == str(ctx.message.author))
        bet = bets.get((query.user == str(ctx.message.author)) & (query.line.matches('^' + re.escape(userLine) + '$', re.IGNORECASE)))

        if user is None:
            await ctx.send("You are not registered")
        elif line is None:
            await ctx.send("{} is not an open line".format(userLine))
        elif bet is None:
            await ctx.send("You do not have a bet on {}".format(line['line']))
        elif line['locked']:
            await ctx.send("The betting is locked for {}".format(line['line']))
        else:
            bets.remove((query.user == str(ctx.message.author)) & (query.line.matches('^' + re.escape(userLine) + '$', re.IGNORECASE)))

            await ctx.send("{0} has cancelled their bet on {1}".format(str(ctx.message.author), line['line']))
    else:
        emoji = get(bot.get_all_emojis(), name='nou')
        await bot.add_reaction(ctx.message, emoji)
        return

@bot.command(pass_context=True, brief="", description="")
async def rand(ctx, amount="0", picked_line_name=""):

    if amount == "0":
        amount = str(random.randint(1,1001))
        #amount = str(random.randint(1,101))

    if amount == "a positive integer":
        await ctx.send("I bet you think your pretty fuckin clever don't you? Fuck off ya cheeky twat.")
        return
    elif not amount.isdigit():
        await ctx.send("Your bet must be a positive integer. Dumb Bitch")
        return
    elif int(amount) > 1000:
        await ctx.send("The max bet is 1000 RABucks")
        return

    # not own
    # not already bet upon
    # not locked

    myBets = bets.search(query.user == str(ctx.message.author))
    myLines = list(map(lambda x: x['line'].lower(), myBets))
    allLines = list(map(lambda x: x['line'], lines.search((query.locked == False) & (query.host != str(ctx.message.author)))))

    notMyLines = []

    for line in allLines:
        if not line.lower() in myLines:
            notMyLines.append(line)

    if len(notMyLines) > 0:
        randomLine = random.choice(notMyLines)
        randomPosition = random.choice(["over", "under"])
    else:
        await ctx.send("There are no eligible lines for you to bet on")
        return;

    if picked_line_name == "":
        await overunder(ctx, randomLine, amount, randomPosition)
    elif not picked_line_name.lower() in list(map(lambda x: x.lower(), notMyLines)):
        await ctx.send("{} is not an eligible line".format(picked_line_name))
    else:
        await overunder(ctx, picked_line_name, amount, randomPosition)

@bot.command(pass_context=True, aliases = ["RandAll", "randAll", "box"], brief="", description="")
async def randall(ctx, amount="0"):

    if amount == "0":
        amount = str(random.randint(1,1001))

    if amount == "a positive integer":
        await ctx.send("I bet you think your pretty fuckin clever don't you? Fuck off ya cheeky twat.")
        return
    elif not amount.isdigit():
        await ctx.send("Your bet must be a positive integer. Dumb Bitch")
        return
    elif int(amount) > 1000:
        await ctx.send("The max bet is 1000 RABucks")
        return

    myBets = bets.search(query.user == str(ctx.message.author))
    myLines = list(map(lambda x: x['line'].lower(), myBets))
    allLines = list(map(lambda x: x['line'], lines.search((query.locked == False) & (query.host != str(ctx.message.author)))))

    notMyLines = []

    for line in allLines:
        if not line.lower() in myLines:
            notMyLines.append(line)

    for randomLine in notMyLines:
        randomPosition = random.choice(["over", "under"])
        await overunder(ctx, randomLine, amount, randomPosition, True)

    await myLinesFunc(ctx)

@bot.command(pass_context=True, brief ="", description="")
async def autogame(ctx, favored_team, underdog, spread, over_under, locktime):
    localtime = functions.my_parser(locktime)
    dt = parser.parse(functions.from_time(localtime))
    if (str(ctx.message.author) in whitelist):
        await houseLine(ctx, "{0}{1}spread".format(favored_team, underdog), "{0} beats {1} by {2}. Line locks at {3}.".format(favored_team, underdog, spread, functions.to_time(dt)), dt)
        await houseLine(ctx, "{0}{1}OU".format(favored_team, underdog), "{0} and {1} have a combined score of {2}. Line locks at {3}.".format(favored_team, underdog, over_under, functions.to_time(dt)), dt)
    else:
        await ctx.send("Only whitelisted users can perform this action")

@bot.command(pass_context=True, brief ="", description="")
async def game(ctx, favored_team, underdog, spread, over_under):

    #Verify Spread and over_under are reasonable
    #Make sure these lines haven't been opened before

    if (str(ctx.message.author) in whitelist):
        await houseLine(ctx, "{0}{1}spread".format(favored_team, underdog), "{0} beats {1} by {2}. Line locks at Kickoff.".format(favored_team, underdog, spread))
        await houseLine(ctx, "{0}{1}OU".format(favored_team, underdog), "{0} and {1} have a combined score of {2}. Line locks at Kickoff.".format(favored_team, underdog, over_under))
    else:
        await ctx.send("Only whitelisted users can perform this action")

@bot.command(pass_context=True, brief="", description="")
async def over(ctx, userLine, amount):
    await overunder(ctx, userLine, amount, "over")

@bot.command(pass_context=True, brief="", description="")
async def under(ctx, userLine, amount):
    await overunder(ctx, userLine, amount, "under")

@bot.command(pass_context=True, brief="", description="")
async def nou(ctx, user: discord.Member = None):
    if (user is None):
        emoji = bot.get_emoji(484065982025826304)
        await ctx.send(emoji)
    elif (str(ctx.message.author) == "box_of_rockz#2813"):
        await ctx.send("Fuck Off Box")
    elif (str(ctx.message.author) == "pollytheparrot#4919"):
        await ctx.send("This is not for you Polly")
    elif (str(ctx.message.author) in modlist):
        emoji = get(bot.get_all_emojis(), name='nou')
        await ctx.send("{0} {1}".format(user.mention, emoji))
    elif (str(user) in modlist):
        await ctx.send("**I WILL NOT TURN ON MY MASTER**")
    elif (str(ctx.message.author) == str(user)):
        await ctx.send("Fuck off")
    else:
        await ctx.send("{} No u".format(ctx.message.author.mention))

@bot.command(pass_context=True, brief="", description="")
async def pinksock(ctx):
    emoji = get(bot.get_all_emojis(), name='pinksock')
    await ctx.send(emoji)

@bot.command(pass_context=True, brief="", description="")
async def free(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://media.giphy.com/media/5wWf7GMbT1ZUGTDdTqM/giphy.gif')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def neat(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://i.imgur.com/Y4YFthE.gif')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def bronze(ctx):
    await bronzeFunc(ctx)

@bot.command(pass_context=True, brief="", description="")
async def RAbronze(ctx):
    await bronzeFunc(ctx)

async def bronzeFunc(ctx):
    embed = discord.Embed(color=0xCD7F32)
    embed.set_image(url='https://i.imgur.com/XznfKMo.png')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def moron(ctx):
    embed = discord.Embed(color=0xc0c0c0)
    embed.set_image(url='https://cdn.discordapp.com/attachments/464871290595966996/615010318707326994/image0.jpg')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def silver(ctx):
    embed = discord.Embed(color=0xc0c0c0)
    embed.set_image(url='https://i.imgur.com/m1PudkI.jpg')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="", description="")
async def Bart(ctx):
    await bart_meme_func(ctx)

@bot.command(pass_context=True, brief="", description="")
async def bartdad(ctx):
    await bart_meme_func(ctx)

async def bart_meme_func(ctx):
    embed = discord.Embed(color=0x00cc00)
    meme_list = memes.all()
    random.shuffle(meme_list)
    embed.set_image(url=meme_list[0]['link'])
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Information about the Open Source Repo", description="Shows information about The Don bot and links to the repo location", aliases = ["git", "github", "opensource", "openSource"])
async def contribute(ctx):
    await contributeFunc(ctx)

async def contributeFunc(ctx):
    await ctx.send("The Don is now Open source\r\nhttps://github.com/ArtificialBadger/TheDon")

@bot.command(pass_context=True, brief="", description="")
async def zoopking(ctx):

    message = await ctx.send(':point_up: :sunglasses: :point_up:')

    for x in range(5):

        await asyncio.sleep(.25)

        if x % 4 == 0:
            await message.edit(content=':point_left: :sunglasses: :point_left:')

        elif x % 4 == 1:
            await message.edit(content=':point_down: :sunglasses: :point_down:')

        elif x % 4 == 2:
            await message.edit(content=':point_right: :sunglasses: :point_right:')

        elif x % 4 == 3:
            await message.edit(content=':point_up: :sunglasses: :point_up:')

@bot.command(pass_context=True, brief="", description="")
async def zoopsalute(ctx):

    message = await ctx.send(':point_up: :sunglasses: :point_up: :point_up: :sunglasses: :point_up:')

    for x in range(5):

        await asyncio.sleep(.25)

        if x % 4 == 0:
            await message.edit(content=':point_right: :sunglasses: :point_right: :point_left: :sunglasses: :point_left:')

        elif x % 4 == 1:
            await message.edit(content=':point_down: :sunglasses: :point_down: :point_down: :sunglasses: :point_down:')

        elif x % 4 == 2:
            await message.edit(content=':point_left: :sunglasses: :point_left: :point_right: :sunglasses: :point_right:')

        elif x % 4 == 3:
            await message.edit(content=':point_up: :sunglasses: :point_up: :point_up: :sunglasses: :point_up:')



@bot.command(pass_context=True, brief="", description="")
async def zoop(ctx):
    await ctx.send(':point_left: :sunglasses: :point_left:')


@bot.command(pass_context=True, brief="", description="")
async def pooz(ctx):
    await ctx.send(':point_right: :sunglasses: :point_right:')

@bot.command(pass_context=True, brief="", description="")
async def frank(ctx):
    emoji = get(bot.get_all_emojis(), name='bigfrank')
    await ctx.send(emoji)

@bot.command(pass_context=True, brief="", description="")
async def bigfrank(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://i.imgur.com/N5bjEMl.png')
    await ctx.send(embed=embed)

@bot.command(pass_context=True, brief="Checks the bots status")
async def health(ctx):
    await ctx.send("Up and Running! " + str(instance_id))

@bot.command(pass_context=True, brief="Stops an instance of the bot if with the given ID")
async def stop(ctx, kill_id):
    if (str(ctx.message.author) in modlist):
        if kill_id == str(instance_id):
            await ctx.send("Stopping Don with ID " + str(instance_id))
            await bot.logout()
        else:
            await ctx.send("Not stopping Don with ID " + str(instance_id))
    else:
        await ctx.send("Only mods can stop The Don bot")

print("start")
bot.run(app_secret)
print("stop")
