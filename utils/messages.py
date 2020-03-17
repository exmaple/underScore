import discord


def embedded_stats(title, **stats):
    """Build embedded message with player statistics

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


def embedded_matchday_results(matchday, matches):
    """Build embedded message with matchday results"""
    title = "Matchday " + matchday
    embed = discord.Embed(title=title, color=0xDC052D)

    for key, value in matches.items():
        # where value is a list of of 2 tuples
        # each tuple contains: ('team_name', 'score')
        embed.add_field(
            name=value[0][0] + "-" + value[1][0],
            value=value[0][1] + "-" + value[1][1],
            inline=True,
        )

    return embed
