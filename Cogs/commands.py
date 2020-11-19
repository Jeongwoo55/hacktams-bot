from discord.ext.commands import Cog, command, group
from discord import Embed, Color


class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log.getChild(type(self).__name__)
        self.urls = bot.config["urls"]

    def embed(self, item):
        url = self.urls.get(item, self.urls["base"]+item) # gets either the set <item> or the base / <item>
        return Embed(title=f"{item} url", description=url, url=url)

    @command()
    async def ip(self, ctx):
        pass  # I have no idea what this does

    @command()
    async def devpost(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))

    @command()
    async def discord(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))

    @command()
    async def zoom(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))

    @command()
    async def livesite(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))

    @command()
    async def info(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))

    @command()
    async def schdule(self, ctx):
        await ctx.send(embed=self.embed(ctx.command.name))


setup = lambda bot: bot.add_cog(Commands(bot))
