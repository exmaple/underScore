import discord
import logging

logger = logging.getLogger("app")


def title_card():

    logger.info("Sending help")

    embed = discord.Embed(title="Help Info", color=0xFFFF72)

    embed.add_field(
        name="How to use commands:", value="`![command] [arg1 arg2 ...]`", inline=False
    )

    return embed


def embedded_help(command):
    embed = discord.Embed(title="`" + command.name + "`", color=0xFFFF72)
    args = "> "
    try:
        for arg_tuple in command.usage:
            if command.usage.index(arg_tuple) == len(command.usage) - 1:
                args += arg_tuple[0] + ": " + arg_tuple[1] + "\n"
            else:
                args += arg_tuple[0] + ": " + arg_tuple[1] + "\n > "
    except TypeError:
        args = "No Args"

    embed.add_field(
        # name=f"{command}",
        name="__Arguments:__",
        value=args,
        inline=False,
    )

    return embed
