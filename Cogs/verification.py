from discord.ext.commands import Cog, command, group, dm_only, check_any, has_permissions
from discord import Embed, Color, Member


class Verification(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log.getChild(type(self).__name__)
        
    async def _verify(self, member, auto=True):
        await ctx.send(embed=Embed(title='Welcome to HackTAMS', color=Color.orange(), description='To start the verification process enter the email you used to register for hackTAMS\nEx: `hackerduck@hacktams.org`').set_footer(text="If you haven't registered yet you can do so at hacktams.org/register"))
        msg = await self.bot.wait_for('message',timeout=60 * (int(auto)+1) check=lambda msg:msg.author.id==member.id, msg.channel.id==member.id)
        
    @Cog.listener()
    async def on_member_join(self, member):  # put the member data into storage
        self.log.info(f"{member.name} has joined {member.guild.name}")

        await self._verify(member)

    @command()
    @check_any(dm_only(), has_permissions(administrator=True))
    async def verify(self, ctx, member:Member=None):
        if not ctx.channel:
            member = ctx.author 
        member = member or ctx.author 

        await self._verify(member, auto=False)

    @Cog.listener()
    async def on_member_leave(
        self, member
    ):  # move the member out of storage (?) might not
        self.log.info(f"{member.name} has left {member.guild.name}")

    @Cog.listener()
    async def on_member_verify(
        self, member, data
    ):  # whenever a user verifies we can edit stuff on them like roles
        await member.edit(name=data["name"])


setup = lambda bot: bot.add_cog(Verification(bot))
