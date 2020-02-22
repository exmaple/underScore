import discord
from discord.ext import commands
from random import choice, randrange

from utils.messages import embedded_stats
from utils.dummy_data import get_dummy_data


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def getStats(self, ctx, player_name):
        height, weight, position, gp, goals, assists = get_dummy_data()
        embed = embedded_stats(
            player_name,
            height=height,
            weight=weight,
            position=position,
            gp=gp,
            goals=goals,
            assists=assists,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
