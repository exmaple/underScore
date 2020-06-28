import discord

def help_title_card():
    embed = discord.Embed(title='Help Info', color=0xffff72)

    embed.add_field(
        name='How to use commands:',
        value='![command] [option1 option2 ...]',
        inline=False
    )

    return embed

def embedded_help_command(command):
    embed = discord.Embed(title='`'+command.name+'`', color=0xffff72)
    args = '> '
    try:
        for arg_tuple in command.usage:
            if command.usage.index(arg_tuple) == len(command.usage)-1:
                args += arg_tuple[0] +': '+ arg_tuple[1] +'\n'
            else:
                args += arg_tuple[0] +': '+ arg_tuple[1] +'\n > '
    except TypeError:
        args='No Args'

    embed.add_field(
        # name=f"{command}\n",
        name='__Options:__',
        value=args,
        inline=False
    )

    return embed


def embedded_stats(title, **stats):
    """Build embedded message with generic statistics

    Args:
        title (str): title of the embedded message
        **stats (dict): all stats to add as fields

    Returns:
        embed message object
    """
    embed = discord.Embed(title=title, color=0xDC052D)
    embed.set_thumbnail(url="https://clipartart.com/images/bavaria-logo-clipart.jpg")

    for name, stat in stats.items():
        embed.add_field(name=name, value=stat, inline=True)

    return embed


def embedded_matchday_results(matchday, season, matchdays, matchdate):
    """Build embedded message with matchday results

    Args:
        matchday (string): a number representing the matchday (eg. '2')
        matches (dict): dictionary containing team matchups and the corresponding score
            e.g. {0: [('Team Name 1', 'Score'),('Team Name 2', 'Score')], ... }

    Returns:
        embed message object
    """
    pre_season = int(season)-1
    season = str(pre_season) +'\/'+ season
    title = "Matchday " + matchday + "  " + season
    embed = discord.Embed(title=title, description=matchdate, color=0xDC052D)
    for match in matchdays[matchdate]:
        embed.add_field(
            name=match[0][0] + " - " + match[1][0],
            value=match[0][1] + ":" + match[1][1],
            inline=False,
        )

    return embed
