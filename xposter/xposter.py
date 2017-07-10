import discord
from discord.ext import commands

import re

XPOST = re.compile('x-?post #(?P<channel>\w+)', re.IGNORECASE)


class Xposter:
    """Bot that detects x-posts and dispatches them to desired channels"""

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.server is None or self.bot.user == message.author:
            return

        if XPOST.match(message.content):
            for channel in message.channel_mentions:
                self.xpost(message, channel)

    async def xpost(message, channel):
        content = "Detected x-post from @{} in {}: {}".format(
            message.author, message.channel, message.content)
        await self.bot.send_message(channel, content)


def setup(bot):
    xposter = Xposter(bot)
    bot.add_listener(xposter.on_message, 'on_message')
    bot.add_cog(xposter)
