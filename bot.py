from discord.ext.commands import Bot, MinimalHelpCommand

class BetterHelp(MinimalHelpCommand):  # making our own interactive help command to support embeds
    def get_command_signature(self, command):
        return "{0.clean_prefix}{1.qualified_name} {1.signature}".format(self, command)

    async def command_callback(self, ctx, *, command=None):
        """|coro|
        The actual implementation of the help command.
        It is not recommended to override this method and instead change
        the behaviour through the methods that actually get dispatched.
        - :meth:`send_bot_help`
        - :meth:`send_cog_help`
        - :meth:`send_group_help`
        - :meth:`send_command_help`
        - :meth:`get_destination`
        - :meth:`command_not_found`
        - :meth:`subcommand_not_found`
        - :meth:`send_error_message`
        - :meth:`on_help_command_error`
        - :meth:`prepare_help_command`
        """
        await self.prepare_help_command(ctx, command)
        bot = ctx.bot

        if command is None:
            mapping = self.get_bot_mapping()
            return await self.send_bot_help(mapping)

        # Check if it's a cog
        for cog in bot.cogs.keys():
            if cog.lower() == command.lower():  # ignore capitalization
                return await self.send_cog_help(bot.get_cog(cog))

        maybe_coro = discord.utils.maybe_coroutine

        # If it's not a cog then it's a command.
        # Since we want to have detailed errors when someone
        # passes an invalid subcommand, we need to walk through
        # the command group chain ourselves.
        keys = command.split(" ")
        cmd = bot.all_commands.get(keys[0])
        if cmd is None:
            string = await maybe_coro(
                self.command_not_found, self.remove_mentions(keys[0])
            )
            return await self.send_error_message(string)

        for key in keys[1:]:
            try:
                found = cmd.all_commands.get(key)
            except AttributeError:
                string = await maybe_coro(
                    self.subcommand_not_found, cmd, self.remove_mentions(key)
                )
                return await self.send_error_message(string)
            else:
                if found is None:
                    string = await maybe_coro(
                        self.subcommand_not_found, cmd, self.remove_mentions(key)
                    )
                    return await self.send_error_message(string)
                cmd = found

        if isinstance(cmd, Group):
            return await self.send_group_help(cmd)
        else:
            return await self.send_command_help(cmd)

    async def command_not_found(self, string):
        dest = self.get_destination()
        ctx = self.context
        return "I can't find that command!"

    async def send_group_help(self, group):
        ctx = self.context

        filtered = await self.filter_commands(group.commands, sort=self.sort_commands)
        lines = []
        if filtered:
            for command in filtered:
                lines.append(
                    f"**{ctx.prefix}{command.full_parent_name} {command.name}** - {command.short_doc}"
                )
        embed = Embed(color=ctx.me.color, title=f"{ctx.guild.name}")

        embed.set_author(
            name=f"{bot.user.name} Help Manual",
            icon_url=bot.user.avatar_url_as(format="png"),
        )
        await LinePaginator.paginate(
            (line for line in lines),
            self.get_destination(),
            embed,
            bot,
            max_lines=100,
            max_size=1000,
            empty=False,
        )

    async def send_bot_help(self, mapping):
        ctx = self.context
        # pprint(vars(ctx))
        bot = ctx.bot

        lines = []

        no_category = "\u200b{0.no_category}:".format(self)

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.name + ":" if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, commands in to_iterate:
            commands = (
                sorted(commands, key=lambda c: c.name)
                if self.sort_commands
                else list(commands)
            )
            lines.append(
                f"**{category}**\n" + ", ".join([f"`{c.name}`" for c in commands])
            )

        embed = Embed(
            color=ctx.author.color,
            description="\n".join(lines),
        )

        embed.set_author(
            name=f"{bot.user.name} Help Manual",
            icon_url=bot.user.avatar_url_as(format="png"),
        )
        embed.set_footer(text=f"to edit configurations run {ctx.prefix}plugins")
        destination = self.get_destination()
        return await destination.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        bot = ctx.bot

        destination = self.get_destination()
        lines = []

        filtered = await self.filter_commands(
            cog.get_commands(), sort=self.sort_commands
        )
        lines.append(f"**__{cog.description}__**")
        for command in filtered:
            lines.append(f"**{ctx.prefix}{command.name}** - {command.short_doc}")

        note = self.get_ending_note() or None
        if not note:
            note = ""

        lines.append(f"**{ctx.prefix}{command.name}** - {command.description}")

        embed = Embed(color=ctx.me.color, title=f"{ctx.guild.name}")

        embed.set_author(
            name=f"{bot.user.name} Help Manual",
            icon_url=bot.user.avatar_url_as(format="png"),
        )
        await LinePaginator.paginate(
            (line for line in lines),
            destination,
            embed,
            bot,
            footer_text=note,
            max_lines=10,
            empty=False,
        )

    async def send_command_help(self, command):
        ctx = self.context
        try:
            stat = await command.can_run(ctx)
        except:
            stat = True
        finally:
            if not stat:
                raise CommandError("You do not have the permssions to run that command")
        bot = ctx.bot
        destination = self.get_destination()

        note = self.get_ending_note()
        if not note:
            note = ""
        embed = Embed(color=ctx.me.color, title=f"{ctx.guild.name}")
        embed.set_author(
            name=f"{bot.user.name} Help Manual",
            icon_url=bot.user.avatar_url_as(format="png"),
        )
        embed.set_footer(text=note)
        embed.description = (
            f"**__{ctx.prefix}{command.qualified_name}__**\n{command.help}\n"
            f"**Usage**: {ctx.prefix}{command.usage or command.qualified_name}"
        )
        if command.aliases is not None:
            embed.description += f"\n\n**Aliases:** {', '.join(command.aliases)}"
        await destination.send(embed=embed)


class HackTamsBot(Bot): #inheriting from discord.py's ext.commands.Bot
  pass
  
bot = HackTamsBot()
bot.run(reconnect=True)
