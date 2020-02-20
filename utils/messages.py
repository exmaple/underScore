import discord


def embedded_stats(title, **stats):
    """Build embedded message with player statistics"""
    embed = discord.Embed(title=title, color=0xDC052D)
    embed.set_thumbnail(url="https://clipartart.com/images/bavaria-logo-clipart.jpg")

    for name, stat in stats.items():
        embed.add_field(name=name, value=stat, inline=True)

    return embed
