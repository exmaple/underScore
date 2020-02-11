import discord
from discord.ext import commands


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)


def setup(client):
    client.add_cog(Example(client))
