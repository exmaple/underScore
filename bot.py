import discord
from discord.ext import commands
import os
import click
import logging
import sys


logger = logging.getLogger("app")


def setup_logging(log_level):
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level))


def load_extensions(bot, extensions):
    """Load the extensions to the bot instance

    Args:
        bot (Bot): bot instance to load extensions to
        extensions (list): all the extensions to load
    """
    for extension in extensions:
        try:
            bot.load_extension(extension)
            logger.debug(f"Extension {extension} loaded")
        except Exception as error:
            logger.debug(f"{error}")


@click.command()
@click.option("--token", default=None, help="Token from the developer portal")
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["INFO", "DEBUG", "WARNING", "ERROR"], case_sensitive=False),
)
def main(token, log_level):
    setup_logging(log_level)

    logger.info("Setting up bot")
    bot = commands.Bot(command_prefix="!")
    bot.remove_command('help') # required to use custom help command

    @bot.event
    async def on_ready():
        """Change bot display message once online"""
        await bot.change_presence(activity=discord.Game(name="!help"))
        logger.info("Bot online")

    extensions = ["cogs.stats_commands"]
    load_extensions(bot, extensions)

    if not token:
        token = os.environ["TOKEN"]

    bot.run(f"{token}")


if __name__ == "__main__":
    main()
