import discord
from discord.ext import commands
from argparse import ArgumentParser
import os


# Get token from command line for now
parser = ArgumentParser()
parser.add_argument(
    "--token",
    "-t",
    action="store",
    required=True,
    help="Token from the developer portal",
)
args = parser.parse_args()

# Simple bot setup
client = commands.Bot(command_prefix="!")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(f"{args.token}")
