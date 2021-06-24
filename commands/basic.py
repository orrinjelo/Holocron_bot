import discord
import asyncio
import random
import aiohttp
import re
from discord.ext import commands
from config.secrets import *
from utils.checks import embed_perms, cmd_prefix_len
import logging
from urllib import parse
from urllib.request import Request, urlopen

logger = logging.getLogger('discord')

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop, headers={"User-Agent": "AppuSelfBot"})

    @commands.command()
    async def flipcoin(self, ctx):
        if self.coinflip() == 0:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")


    @commands.command(aliases=['user', 'uinfo', 'info', 'ui'])
    async def userinfo(self, ctx, *, name=""):
        """Get user info. Ex: ?info user"""
        if ctx.invoked_subcommand is None:
            pre = cmd_prefix_len()
            if name:
                try:
                    user = ctx.message.mentions[0]
                except:
                    user = ctx.guild.get_member_named(name)
                if not user:
                    user = ctx.guild.get_member(int(name))
                if not user:
                    await ctx.send('Could not find user.')
                    return
            else:
                user = ctx.message.author

            # Thanks to IgneelDxD for help on this
            if str(user.avatar_url)[54:].startswith('a_'):
                avi = 'https://images.discordapp.net/avatars/' + str(user.avatar_url)[35:-10]
            else:
                avi = user.avatar_url

            role = user.top_role.name
            if role == "@everyone":
                role = "N/A"
            voice_state = None if not user.voice else user.voice.channel
            if embed_perms(ctx.message):
                em = discord.Embed(timestamp=ctx.message.created_at, colour=0x708DD0)
                em.add_field(name='User ID', value=user.id, inline=True)
                em.add_field(name='Nick', value=user.nick, inline=True)
                em.add_field(name='Status', value=user.status, inline=True)
                em.add_field(name='In Voice', value=voice_state, inline=True)
                em.add_field(name='Game', value=user.activity, inline=True)
                em.add_field(name='Highest Role', value=role, inline=True)
                em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                em.set_thumbnail(url=avi)
                em.set_author(name=user, icon_url='https://i.imgur.com/RHagTDg.png')
                await ctx.send(embed=em)
            else:
                msg = '**User Info:** ```User ID: %s\nNick: %s\nStatus: %s\nIn Voice: %s\nGame: %s\nHighest Role: %s\nAccount Created: %s\nJoin Date: %s\nAvatar url:%s```' % (user.id, user.nick, user.status, voice_state, user.activity, role, user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), avi)
                await ctx.send(msg)

            await ctx.message.delete()

    @commands.command()
    async def avi(self, ctx, txt: str = None):
        """View bigger version of user's avatar. Ex: ?avi @user"""
        if txt:
            try:
                user = ctx.message.mentions[0]
            except:
                user = ctx.guild.get_member_named(txt)
            if not user:
                user = ctx.guild.get_member(int(txt))
            if not user:
                await ctx.send('Could not find user.')
                return
        else:
            user = ctx.message.author

        # Thanks to IgneelDxD for help on this
        if str(user.avatar_url)[54:].startswith('a_'):
            avi = 'https://images.discordapp.net/avatars/' + str(user.avatar_url)[35:-10]
        else:
            avi = user.avatar_url
        if embed_perms(ctx.message):
            em = discord.Embed(colour=0x708DD0)
            em.set_image(url=avi)
            await ctx.send(embed=em)
        else:
            await ctx.send(avi)
        await ctx.message.delete()            

    @commands.command(pass_context=True, aliases=['updawg'])
    @commands.has_role(BOT_ADMIN_ROLE)
    @commands.has_role("BotAdmin")
    async def update(self, ctx):
        latest = update_bot(True)
        if latest:
            g = git.cmd.Git(working_dir=os.getcwd())
            g.execute(["git", "pull", "origin", "master"])
            try:
                await ctx.send(content=None, embed=latest)
            except:
                pass
            await ctx.send('Downloading update...')
        else:
            await ctx.send('No updates available.')

    @commands.command(pass_context=True, aliases=['reboot', 'reload'])
    @commands.has_role(BOT_ADMIN_ROLE)
    @commands.has_role("BotAdmin")
    async def restart(self, ctx):
        """Restarts the bot."""
        latest = update_bot(True)
        if latest:
            g = git.cmd.Git(working_dir=os.getcwd())
            g.execute(["git", "pull", "origin", "master"])
            try:
                await ctx.send(content=None, embed=latest)
            except:
                pass
            with open('quit.txt', 'w', encoding="utf8") as q:
                q.write('update')
            print('Downloading update and restarting...')
            await ctx.send('Downloading update and restarting (check your console to see the progress)...')

        else:
            print('Restarting...')
            with open('restart.txt', 'w', encoding="utf8") as re:
                re.write(str(ctx.message.channel.id))
            await ctx.send('Restarting...')

        # if self.bot.subpro:
        #     self.bot.subpro.kill()
        os._exit(0)