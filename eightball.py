#!/usr/bin/python3.6
import discord
from discord.ext import commands
from tinydb import TinyDB, Query, where
from models import Answer


class EightBall(commands.Cog):

    eightball = TinyDB('8ball.json')

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        await ctx.send('Hello from a Cog')

    @bot.command(pass_context=True)
    async def respond(ctx, *, response):
        global eightball
        current_answer_list = eightball.search(query.name == response)
        if len(current_answer_list) > 0:
            await ctx.send("Thats already a response");
        else:
            eightball.insert(vars(Answer(response)))
            await ctx.send("Registered new response!");

