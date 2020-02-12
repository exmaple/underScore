import discord
from discord.ext import commands, tasks
from itertools import cycle

status = cycle(["!help for more details", "!setup to configure bot"])


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Tasks
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Bot is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    # Error handlers
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specifiy the number of messages to delete.")


def setup(client):
    client.add_cog(Example(client))
