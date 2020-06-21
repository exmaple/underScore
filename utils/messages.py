import discord


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

    title = "Matchday " + matchday + "  " + season
    embed = discord.Embed(title=title, description=matchdate, color=0xDC052D)
    for match in matchdays[matchdate]:
        embed.add_field(
            name=match[0][0] + " - " + match[1][0],
            value=match[0][1] + ":" + match[1][1],
            inline=False,
        )

    return embed
