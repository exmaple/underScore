import discord
from discord.ext import commands
from random import choice, randrange

from utils.messages import embedded_player_stats


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, player_name):
        info = {
            "height": randrange(150, 200),
            "weight": randrange(50, 110),
            "position": choice(["GK", "CB", "CM", "ST"]),
        }
        stats = {
            "gp": randrange(1, 50),
            "goals": randrange(50),
            "assists": randrange(50),
        }
        embed = embedded_player_stats(player_name, info, stats)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
