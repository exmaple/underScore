import discord
from discord.ext import commands
from random import choice, randrange
import logging

from utils.help_embedder import title_card, embedded_help
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

    @commands.command(name="help")
    async def help(self, ctx):
        """
            command.usage is a list containing one tuple for every command argument
                eg. usage=[('arg', 'description')]
        """

        embed = title_card()
        await ctx.send(embed=embed)
        for command in self.bot.commands:
            if command.name != "help":
                embed = embedded_help(command)
                await ctx.send(embed=embed)

    @commands.command(
        description="Returns the statistics for given player",
        usage=[("player_name", "name of the player")],
    )
    async def getStats(self, ctx, player_name):
        """Returns the statistics for given player

        Args:
            ctx (Context): command usage context
            player_name (str): name of the player
        """
        if logger.level == getattr(logging, "INFO"):
            await ctx.message.delete()

        stats = get_dummy_data(player_name)
        stats.update(get_author_info(ctx))
        embed = dict_to_embed(stats)
        logger.info("Sending player stats")
        await ctx.send(embed=embed)

    @commands.command(
        description="Returns match scores for all matches on a specific matchday. Default is current matchday.",
        usage=[
            ("matchday", "A number representing the matchday to lookup (eg. '23')"),
            ("season", "Specify a season (eg. 2011/2012). Default is current season."),
        ],
    )
    async def matchday(
        self, ctx, matchday=get_default_matchday(), season=get_default_season()
    ):
        """Returns match scores for all matches on a specific matchday. Default is current matchday.

        Args:
            matchday: a number representing the matchday to lookup (eg. '23')
            season: the latter year of the years relating to the season (eg. '2020' for the 2019/2020 season)
        """
        if logger.level == getattr(logging, "INFO"):
            await ctx.message.delete()

        results = process_results(matchday, season)
        results.update(get_author_info(ctx))
        logger.info("Sending matchday results")
        embed = dict_to_embed(results, inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        name="blurb",
        description="Displays an 'at a glance' view of a teams season",
        usage=[("team", "name of the team")],
    )
    async def blurb(self, ctx, team):
        """Displays an 'at a glance' view of a teams season

        Args:
            ctx (Context): command usage context
            team (str): name of the team
        """
        if logger.level == getattr(logging, "INFO"):
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
