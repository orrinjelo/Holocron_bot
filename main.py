import sys
import discord
from discord.ext.commands.bot import Bot
import asyncio
from config.secrets import *
from commands.basic import *
from commands.sw import *
from utils.checks import load_config
from utils.spiffyText import spiff
import logging
import traceback
from datetime import datetime as dt

try:
    from systemd.journal import JournaldLogHandler
    SYSTEM_D=True
except:
    SYSTEM_D=False


logger = logging.getLogger('discord')

# instantiate the JournaldLogHandler to hook into systemd
if SYSTEM_D:
    journald_handler = JournaldLogHandler()

logging.addLevelName(
    logging.DEBUG,
    spiff(logging.getLevelName(logging.DEBUG), 'yellow'))
logging.addLevelName(
    logging.INFO,
    spiff(logging.getLevelName(logging.INFO), 'cyan'))
logging.addLevelName(
    logging.WARNING,
    spiff(logging.getLevelName(logging.WARNING), 'yellow', 'b'))
logging.addLevelName(
    logging.ERROR,
    spiff(logging.getLevelName(logging.ERROR), 'red'))
logging.addLevelName(
    logging.CRITICAL,
    spiff(logging.getLevelName(logging.CRITICAL), 'red', 'b'))

logging_format = '%(levelname)s %(module)s::%(funcName)s():%(lineno)d: '
logging_format += '%(message)s'
color_formatter = logging.Formatter(logging_format)

if SYSTEM_D:
    journald_handler.setFormatter(color_formatter)
    logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)

class Holocron(Bot):
    async def on_ready(self):
        logger.info('Connected!')
        logger.info('Username: {0.name}\nID: {0.id}'.format(self.user))
        channel = self.get_channel(BOT_DEBUG_CHANNEL)

        await channel.send("I'm alive!")

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
        #ret = super(Bot, self).on_message(message)
        if message.author.id == BOT_ID: # Charlie
            return None #ret

        if 'cat' in message.content.lower() or 'kitty' in message.content.lower():
            await message.add_reaction("🐈")

        await self.process_commands(message)    

    # async def on_message_edit(self, before, after):
    #     fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
    #     channel = self.get_channel(BOT_DEBUG_CHANNEL)
    #     await channel.send(fmt.format(before, after))

    async def on_command_error(self, ctx, ext):
        channel = self.get_channel(BOT_DEBUG_CHANNEL)
        if channel is not None:
            await channel.send('Error: {}'.format(ext))

            em = discord.Embed(timestamp=ctx.message.created_at, colour=0x708DD0)

            em.add_field(name="Message", value="{}".format(ctx.message))
            em.add_field(name="Command", value="{}".format(ctx.command))
            em.add_field(name="Args", value="{}".format(ctx.args))
            em.add_field(name="Kwargs", value="{}".format(ctx.kwargs))
            em.add_field(name="Channel", value="{}".format(ctx.channel))
            em.add_field(name="Invoker", value="{}".format(ctx.author))

            await channel.send(embed=em)

        await ctx.message.add_reaction('⚠')
        logging.error('Error: {}\nTraceback:{}'.format(ctx.message, ctx.command))
           

    async def on_error(self, event, *args, **kwargs):
        logger.error('{}'.format(event))
        channel = self.get_channel(BOT_DEBUG_CHANNEL)
        if channel is not None:
            em = discord.Embed(timestamp=dt.now(), colour=0x708DD0)
            em.add_field(name='Error', value="Error: {}".format(event), inline=True)
            em.add_field(name='Traceback', value="{}".format(str(traceback.format_exc())[:1024]))
            channel = self.get_channel(BOT_DEBUG_CHANNEL)
            await channel.send(embed=em)
        logging.error('Error: {}\nTraceback:{}'.format(event, traceback.format_exc()))


bot = Holocron(load_config()['cmd_prefix'])

bot.add_cog(Basic(bot))
bot.add_cog(StarWars(bot))

bot.run(API_KEY)
