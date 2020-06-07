import discord
from discord.ext import commands
from random import choice, randrange

from utils.messages import embedded_stats, embedded_matchday_results
from utils.dummy_data import get_dummy_data
from the_mines.process.fussballdaten.process_html import get_matchday_results, get_default_matchday


class Stats(commands.Cog):
    """All statistcal commands are collected here

    Attributes:
        bot (Bot): instance of the bot the cog will attach to
    """

    def __init__(self, bot):
        """Initialization method

        Args:
            bot (Bot): bot to attach to
        """
        self.bot = bot

    @commands.command()
    async def getStats(self, ctx, player_name):
        """Returns the statistics for given player

        Args:
            ctx (Context): command usage context
            player_name (str): name of the player
        """
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

    @commands.command()
    async def getMatchdayResults(self, ctx, matchday=get_default_matchday('matchday'), season=get_default_matchday('season')):
        results = get_matchday_results(matchday, season)
        embed = embedded_matchday_results(matchday, results)
        await ctx.send(embed=embed)


def setup(bot):
    """Adds cog (this class) to bot

    Args:
        bot (Bot): bot to add
    """
    bot.add_cog(Stats(bot))
