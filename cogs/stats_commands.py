import discord
from discord.ext import commands
from random import choice, randrange
import logging

from utils.messages import embedded_stats, embedded_matchday_results
from utils.embedder import dict_to_embed
from utils.dummy_data import get_dummy_data
from utils.misc import get_author_info, get_default_matchday, get_default_season
from the_mines.process.fussballdaten.process_matchday import process_results
from the_mines.process.fussballdaten.process_blurb import get_blurb


logger = logging.getLogger("app")


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
        await ctx.message.delete()
        
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
    async def matchday(
        self, ctx, matchday=get_default_matchday(), season=get_default_season()
    ):
        await ctx.message.delete()

        results = process_results(matchday, season)
        for key in results:
            embed = embedded_matchday_results(matchday, season, results, key)
            await ctx.send(embed=embed)

    @commands.command()
    async def blurb(self, ctx, team):
        """Displays an 'at a glance' view of a teams season

        Args:
            ctx (Context): command usage context
            team (str): name of the team
        """
        await ctx.message.delete()

        blurb = get_blurb(team)
        blurb.update(get_author_info(ctx))
        embed = dict_to_embed(blurb)
        logger.info("Sending blurb")
        await ctx.send(embed=embed)


def setup(bot):
    """Adds cog (this class) to bot

    Args:
        bot (Bot): bot to add
    """
    bot.add_cog(Stats(bot))
