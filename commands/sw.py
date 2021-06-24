import discord
import asyncio
import random
import aiohttp
import re
from discord.ext import commands
from config.secrets import *
from utils.checks import embed_perms, cmd_prefix_len
from utils.dice import interpret_dice, dice_to_anim, roll_dice
import logging
from urllib import parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

logger = logging.getLogger('discord')

class StarWars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop, headers={"User-Agent": "AppuSelfBot"})

    @commands.command(aliases=['wp','wiki','wookiepedia'])
    async def wookieepedia(self, ctx, *msg):
        '''Finds an article on Wookieepedia'''
        search = parse.quote(' '.join(msg))
        query = lambda q: "https://starwars.fandom.com/wiki/Special:Search?query={}".format(q)
        try:
            async with self.session.get(query(search)) as page:
                html = await page.read()
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            logger.warning(f'Exception: {e}')
        await ctx.message.delete()
        try:
            link = soup.find_all("article")[1].find_all("a")[0]["href"]
            await ctx.send('{}'.format(link))
        except Exception as e:
            await ctx.send(f"I'm unable to find anything with {search}")
            logger.warning(f'Exception: {e}')

    @commands.command(aliases=["dice", 'r'])
    async def roll(self, ctx, *msg):
        '''Roll SWRPG dice'''

        try:
            dice = interpret_dice(msg)
            if None in dice:
                await ctx.send(f"I don't understand something in that, but I'll do my best.")
        except Exception as e:
            logger.warning(f"Exception: {e}")

        try:
            anim = await ctx.send(f"{''.join(dice_to_anim(dice))}")
            await asyncio.sleep(2)

            dicestr, res = roll_dice(dice)

            await anim.edit(content=f"{dicestr}")
            await ctx.send(f"Result: {res}")
        except Exception as e:
            logger.warning(f'Exception: {e}')
            await ctx.send("I've utterly failed at my job.")

