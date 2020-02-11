import discord
from discord.ext import commands
from argparse import ArgumentParser

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


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")


@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


client.run(f"{args.token}")
