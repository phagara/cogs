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
        self.settings = fileIO('data/typingtrigger/settings.json', 'load')
        self.bagsofdicks = {}

    @commands.group(pass_context=True)
    async def trigger(self, ctx):
        '''
        Configures this bot's typing notification triggers.
        '''
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @trigger.command(pass_context=True, name='add')
    @checks.is_owner()
    async def _trigger_add(self, ctx, trigger: str):
        '''
        Adds a new triggering trigger for typing trigger notification trigger.
        /triggered
        '''
        self.settings['triggers'] = list(
            set(self.settings['triggers']).union(set([trigger])))
        fileIO('data/typingtrigger/settings.json', 'save', self.settings)
        await self.bot.say('Trigger added.')

    @trigger.command(pass_context=True, name='remove')
    @checks.is_owner()
    async def _trigger_remove(self, ctx, trigger: str):
        '''
        Removes an existing triggering text.
        '''
        try:
            self.settings['triggers'].remove(trigger)
        except ValueError:
            await self.bot.say('No such trigger.')
            return

        fileIO('data/typingtrigger/settings.json', 'save', self.settings)
        await self.bot.say('Trigger removed')

    @trigger.command(pass_context=True, name='threshold')
    @checks.is_owner()
    async def _trigger_threshold(self, ctx, threshold: int):
        '''
        Sets the typing notification threshold.
        '''
        self.settings['threshold'] = threshold
        fileIO('data/typingtrigger/settings.json', 'save', self.settings)
        await self.bot.say('Threshold modified.')

    @trigger.command(pass_context=True, name='show')
    async def _trigger_show(self, ctx):
        '''
        Shows a list ofconfigured typing notification triggers.
        '''
        await self.bot.say('Typing notification threshold: {}'.format(
            self.settings['threshold']))
        await self.bot.say('Configured trigger messages:\n\t{}'.format(
            '\n\t'.join(self.settings['triggers'])))

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
        if channel.is_private:
            return
        elif user.id == self.bot.user.id:
            return

        length = self.bagsofdicks.setdefault(
            channel.name, UnCache()).add(user.name)

        if length >= self.settings['threshold']:
            await self.bot.send_typing(channel)


def check_folder():
    if not os.path.exists('data/typingtrigger'):
        os.makedirs('data/typingtrigger')


def check_file():
    if not fileIO('data/typingtrigger/settings.json', 'check'):
        fileIO('data/typingtrigger/settings.json', 'save',
               {'triggers': [],
                'threshold': 3})


def setup(bot):
    check_folder()
    check_file()
    typingtrigger = TypingTrigger(bot)
    bot.add_listener(typingtrigger.handle_message, 'on_message')
    bot.add_listener(typingtrigger.handle_typing, 'on_typing')
    bot.add_cog(typingtrigger)
