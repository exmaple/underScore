import discord
from discord.ext import commands
from argparse import ArgumentParser
import os


def load_extensions(bot, extensions):
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
        await bot.change_presence(activity=discord.Game(name="!help"))
        print("Bot online")

    extensions = ["cogs.stats_commands"]
    load_extensions(bot, extensions)

    if args.token:
        run_token = args.token
    else:
        run_token = os.environ["TOKEN"]

    bot.run(f"{run_token}")
