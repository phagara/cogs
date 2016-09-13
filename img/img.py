import os
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import fileIO
from apiclient.discovery import build


class GoogleImageSearch:
    """I'm feeling lucky google image search"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/img/settings.json", "load")

    def save_settings(self):
        fileIO("data/img/settings.json", "save", self.settings)

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def imgsetkey(self, ctx, apikey: str):
        """Server API key for search requests"""
        server = ctx.message.server

        if not server:
            await self.bot.reply("You need to type this on a server, sorry.")
            return

        if server.id not in self.settings:
            self.settings[server.id] = {}

        self.settings[server.id]["apikey"] = apikey
        self.save_settings()
        await self.bot.reply("Google server API key saved.")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def imgsetcx(self, ctx, cx: str):
        """Google Custom Search Engine ID for search requests"""
        server = ctx.message.server

        if not server:
            await self.bot.reply("You need to type this on a server, sorry.")
            return

        if server.id not in self.settings:
            self.settings[server.id] = {}

        self.settings[server.id]["cx"] = cx
        self.save_settings()
        await self.bot.reply("Google Custom Search Engine ID saved.")

    @commands.command(pass_context=True, no_pm=True)
    async def img(self, ctx, *query: str):
        """Fetches the first google image search result for a given query."""
        query = ' '.join(query)

        server = ctx.message.server
        if not server:
            await self.bot.reply("You need to type this on a server, sorry.")

        if server.id not in self.settings:
            self.settings[server.id] = {}
            self.save_settings()

        if "apikey" not in self.settings[server.id]:
            await self.bot.reply("Admin needs to set"
                                 " Google server API key first!")
            return
        elif "cx" not in self.settings[server.id]:
            await self.bot.reply("Admin needs to set"
                                 " Google Custom Search Engine ID!")
            return

        service = build("customsearch", "v1",
                        developerKey=self.settings[server.id]["apikey"])

        res = service.cse().list(
            searchType='image',
            q=query,
            cx=self.settings[server.id]["cx"],
            num=1,
            safe='off'
        ).execute()

        if 'items' not in res:
            await self.bot.reply('no result / something went wrong™')
        else:
            title = res['items'][0]['title']
            link = res['items'][0]['link']
            await self.bot.say('{}\n{}'.format(title, link))


def check_folders():
    if not os.path.exists("data/img"):
        print("Creating data/img forder...")
        os.makedirs("data/img")


def check_files():
    f = "data/img/settings.json"
    if not fileIO(f, "check"):
        print("Creating empty data/img/settings.json...")
        fileIO(f, "save", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(GoogleImageSearch(bot))
