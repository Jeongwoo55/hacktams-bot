from discord.ext.commands import Cog, command, group
from discord.ext.tasks import loop


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_event.start()

    @loop(minutes=1)
    async def check_for_event(self):
        pass

    @group()
    async def events(self, ctx):
        pass

    @events.command()
    async def add(self, ctx, event, time):
        pass

    @events.command()
    async def remove(self, ctx, eventname):
        pass

setup = lambda bot: bot.add_cog(Events(bot))