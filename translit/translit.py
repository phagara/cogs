import discord
from discord.ext import commands
import transliterate


class Translit:
    def __init__(self, bot):
        self.bot = bot
        self.avail = transliterate.get_available_language_codes()

    @commands.command(pass_context=True)
    async def translit(self, ctx, target: str, *text: str):
        if target not in self.avail:
            await self.bot.reply("Unknown target language charset code. "
                                 "Supported: {}".format(", ".join(self.avail)))
        else:
            text = " ".join(text)
            await self.bot.reply(transliterate.translit(text, target))
            
    @commands.command(pass_context=True)
    async def untranslit(self, ctx, source: str, *text: str):
        if source not in self.avail:
            await self.bot.reply("Unknown source language charset code. "
                                 "Supported: {}".format(", ".join(self.avail)))
        else:
            text = " ".join(text)
            await self.bot.reply(transliterate.translit(text, source, reversed=True))


def setup(bot):
    bot.add_cog(Translit(bot))
