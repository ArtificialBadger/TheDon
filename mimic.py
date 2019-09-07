#!/usr/bin/python3.6
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import markovify


class Mimic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helloMimic(self, ctx, *, member: discord.Member = None):
        await ctx.send('Hello from the Mimic Cog')

    @commands.command(brief="", description="")
    async def mimic(self, ctx):
        megastring = ""
        count = 0
        async for message in ctx.history(limit=5000, oldest_first=False):
            if str(message.author) == str(ctx.message.author) and not message.content == "" and not message.author.bot:
                if not "$" in message.content:
                    megastring += ". " + message.content
                    count += 1
        if len(megastring) < 10:
            await ctx.send("No can do buckaroo Count: " + str(count) + megastring)
        try:
            chain = markovify.Text(megastring)
            sentence = chain.make_short_sentence(max_chars=64, max_overlap_ratio=.95)
            # await ctx.send("Count: " + str(count))
            if sentence is None:
                raise Exception('Fuck')
            else:
                await ctx.send(sentence)
        except:
            # await ctx.send(megastring)
            await ctx.send("No can do buckaroo")

    @commands.command(brief="", description="")
    async def mimic2(self, ctx):
        megastring = ""
        count = 0
        async for message in ctx.history(limit=5000, oldest_first=False):
            if str(message.author) == str(ctx.message.author) and not message.content == "" and not message.author.bot:
                if (not "$" in message.content):
                    megastring += "\r\n" + message.content
                    count += 1
        if len(megastring) < 10:
            await ctx.send("No can do buckaroo Count: " + str(count) + megastring)
        try:
            chain = markovify.NewlineText(megastring)
            sentence = chain.make_short_sentence(max_chars=100, max_overlap_ratio=.95)
            # await ctx.send("Count: " + str(count))
            if sentence is None:
                raise Exception('Fuck')
            else:
                await ctx.send(sentence)
        except:
            # await ctx.send(megastring)
            await ctx.send("No can do buckaroo")

