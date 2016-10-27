#!/usr/bin/env python3
import os
import logging
import discord
from discord.ext import commands
import transliterate


log = logging.getLogger('red.ScriptBan')


class ScriptBan:
    def __init__(self, bot):
        self.bot = bot
        # scripts: ru,
        # modes: whitelist, blacklist
        # actions: delete, warn
        self.settings = {
            'scripts': {
                'ru': {
                    'mode': 'whitelist',
                    'channels': ['russian'],
                    'action': 'warn',
                },
            },
            'warn': 'Language script `%s` is not allowed in this channel.',
        }

    async def get_action(self, script, channel):
        ''' delete / warn / keep '''
        script_sett = self.settings['scripts'][script]

        mode = script_sett['mode']
        channels = script_sett['channels']
        action = script_sett['action']

        if mode == 'whitelist':
            if channel in channels:
                return 'keep'
            else:
                return action
        elif mode == 'blacklist':
            if channel in channels:
                return 'keep'
            else:
                return action
        else:
            raise ValueError

    async def handle_message(self, message):
        # ignore private messages
        if message.channel.is_private:
            return

        # do not check bot's own messages
        if message.author.id == self.bot.user.id:
            return

        script = transliterate.detect_language(message.clean_content)

        if script not in self.settings['scripts'].keys():
            return

        action = await self.get_action(script, message.channel.name)

        if action == 'keep':
            return
        elif action == 'warn':
            await self.bot.reply(self.settings['warn'].format(script))
        elif action == 'delete':
            await self.bot.delete_message(message)
        else:
            raise ValueError

def setup(bot):
    scriptban = ScriptBan(bot)
    bot.add_listener(scriptban.handle_message, 'on_message')
    bot.add_cog(scriptban)
