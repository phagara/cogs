#!/usr/bin/env python3
import os
import logging
import datetime
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import fileIO
from __main__ import send_cmd_help


log = logging.getLogger('red.TypingTrigger')


class UnCache(object):
    def __init__(self, ttl=datetime.timedelta(seconds=10)):
        self.bag = []
        self.ttl = ttl

    def add(self, item):
        self.bag.append((
            item,
            datetime.datetime.utcnow() + self.ttl
        ))
        return len(self)

    def __len__(self):
        self.bag = [item for item in self.bag
                    if item[1] >= datetime.datetime.utcnow()]
        return len(set([item[0] for item in self.bag]))


class TypingTrigger:
    def __init__(self, bot):
        self.bot = bot
        # TODO: store in a data file
        self.settings = {
            'triggers': [
                '*typing*',
                '**typing**',
                '/me typing',
            ],
        }
        self.bagsofdicks = {}

    # TODO: command to add new triggers

    async def handle_message(self, message):
        if message.channel.is_private:
            # ignore private messages
            return
        elif message.author.id == self.bot.user.id:
            # do not check bot's own messages
            return
        elif message.clean_content not in self.settings['triggers']:
            return
        else:
            await self.bot.send_typing(message.channel)

    async def handle_typing(self, channel, user, when):
        if self.bagsofdicks.setdefault(channel.name, UnCache()).add(user.name) >= 3:
            await self.bot.send_typing(channel)


def setup(bot):
    typingtrigger = TypingTrigger(bot)
    bot.add_listener(typingtrigger.handle_message, 'on_message')
    bot.add_listener(typingtrigger.handle_typing, 'on_typing')
    bot.add_cog(typingtrigger)
