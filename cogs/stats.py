import discord
from discord.ext import commands
from random import choice, randrange

from utils.messages import embedded_player_stats, embedded_team_stats


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player(self, ctx, player_name):
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

    @commands.command()
    async def team(self, ctx, team_name):
        stats = {
            "pos": '1',
            "gp": '22',
            "w": '14',
            "t": '4',
            'l': '4',
            'gf': '62',
            'ga': '24',
            'gd': '38',
            'p': '46'
        }
        embed = embedded_team_stats(team_name, stats)
        await ctx.send(embed)


def setup(bot):
    bot.add_cog(Stats(bot))
