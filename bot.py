import discord
from discord.ext import commands
from argparse import ArgumentParser

# Get token from command line for now
parser = ArgumentParser()
parser.add_argument('--token', '-t', action='store', required=True, help='Token from the developer portal')
args = parser.parse_args()

# Simple bot setup
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot is ready')

client.run(f'{args.token}')
