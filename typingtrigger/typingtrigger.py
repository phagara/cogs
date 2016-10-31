#!/usr/bin/env python3
import os
import logging
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import fileIO
from __main__ import send_cmd_help


log = logging.getLogger('red.TypingTrigger')


class TypingTrigger:
    def __init__(self, bot):
        self.bot = bot
        self.settings = {
            'triggers': [
                '*typing*',
                '**typing**',
                '/me typing',
            ],
        }

    async def handle_message(self, message):
        if message.channel.is_private:
            # ignore private messages
            return
        elif message.author.id == self.bot.user.id:
            # do not check bot's own messages
            return
        elif message.clean_content not in self.settings['triggers']:
            log.info('non-triggering message: %s', message.clean_content)
            return
        else:
            await self.bot.send_typing(message.channel)


def setup(bot):
    typingtrigger = TypingTrigger(bot)
    bot.add_listener(typingtrigger.handle_message, 'on_message')
    bot.add_cog(typingtrigger)
