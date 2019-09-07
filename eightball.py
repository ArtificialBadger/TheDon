#!/usr/bin/python3.6
import discord
from discord.ext import commands
from tinydb import TinyDB, Query, where
from models import Answer
import random

query = Query()
eightball = TinyDB('8ball.json')


class EightBall(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="", description="")
    async def hello8ball(self, ctx, *, member: discord.Member = None):
        await ctx.send('Hello from the EightBall Cog')

    @commands.command(brief="", description="")
    async def respond(self, ctx, *, response):
        global eightball
        current_answer_list = eightball.search(query.name == response)
        if len(current_answer_list) > 0:
            await ctx.send("Thats already a response");
        else:
            eightball.insert(vars(Answer(response)))
            await ctx.send("Registered new response!");

    @commands.command(brief="", description="")
    async def unrespond(self, ctx, *, response):
        eightball.remove(query.response == response)
        await ctx.send("Removed that ish")

    @commands.command(brief="", description="")
    async def ask(self, ctx, *, question):
        answer_list = eightball.all()
        random.shuffle(answer_list)
        await ctx.send(answer_list[0]['response'])
