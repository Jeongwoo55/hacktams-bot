from discord.ext.commands import Cog, command, group


class Music(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log.getChild(type(self).__name__)

    async def do_box_stuff(self, state):
        pass #this is awaited when box joins a voicechannel 

    @Cog.listener()
    async def on_voice_state_update(member, before, after):
        if (member.name = "TheBoxLord#2332") and (before.channel is None) and (after.channel): #I don't have his id sheesh
            await self.do_box_stuff(after)

    @command()
    async def play(self, ctx, song=None):
        pass

    @command()
    async def stop(self, ctx, ctx):
        pass

    @command()
    async def skip(self, ctx, count: int = 1):
        pass

    @command()
    async def queue(self, ctx, page: int = 1):
        pass

    @command()
    async def volume(self, ctx, amount: int):
        pass


setup = lambda bot: bot.add_cog(Music(bot))
