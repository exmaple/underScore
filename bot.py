import discord
from discord.ext import commands
from argparse import ArgumentParser
import os
import click


def load_extensions(bot, extensions):
    """Load the extensions to the bot instance

    Args:
        bot (Bot): bot instance to load extensions to
        extensions (list): all the extensions to load
    """
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Extension {extension} loaded")
        except Exception as error:
            print(f"{error}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--token", "-t", action="store", help="Token from the developer portal",
    )
    args = parser.parse_args()

    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():
        """Change bot display message once online"""
        await bot.change_presence(activity=discord.Game(name="!help"))
        print("Bot online")

    extensions = ["cogs.stats_commands"]
    load_extensions(bot, extensions)

    if args.token:
        run_token = args.token
    else:
        run_token = os.environ["TOKEN"]

    bot.run(f"{run_token}")
