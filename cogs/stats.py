import discord
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player_stats(self, ctx, player_name):
        await ctx.send(f"{player_name} stats")


def setup(bot):
    bot.add_cog(Stats(bot))
