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

def embedded_matchday_results():
    """Build embedded message with matchday results"""
    embed = discord.Embed(title=title, color=0xDC052D)
    embed.set_thumbnail(url="https://clipartart.com/images/bavaria-logo-clipart.jpg")

    for name, stat in stats.items():
        embed.add_field(name=name, value=stat, inline=True)

    return embed
