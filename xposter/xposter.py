import discord
from discord.ext import commands

import logging
import re

XPOST = re.compile('x-?post #(?P<channel>\w+)', re.IGNORECASE)


class Xposter:
    """Bot that detects x-posts and dispatches them to desired channels"""

    log = logging.getLogger('red.Xposter')

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.server is None or self.bot.user == message.author:
            return

        if XPOST.search(message.content):
            self.log.info("Detected XPOST: '%s'", message.content)
            for channel in message.channel_mentions:
                await self.xpost(message, channel)

    async def xpost(self, message, channel):
        content = "Detected x-post from @{} in {}: {}".format(
            message.author, message.channel, message.content)
        await self.bot.send_message(channel, content)


def setup(bot):
    xposter = Xposter(bot)
    bot.add_listener(xposter.on_message, 'on_message')
    bot.add_cog(xposter)
