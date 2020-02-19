import discord
from utils.tables import create_table


def embedded_player_stats(player_name, info, stats):
    """Build embedded message with player statistics"""
    embed = discord.Embed(title=player_name, color=0xDC052D)
    embed.set_thumbnail(url="https://clipartart.com/images/bavaria-logo-clipart.jpg")
    embed.add_field(name="Height (cm)", value=info["height"], inline=True)
    embed.add_field(name="Weight (kg)", value=info["weight"], inline=True)
    embed.add_field(name="Position", value=info["position"], inline=True)
    embed.add_field(name="Games Played", value=stats["gp"], inline=True)
    embed.add_field(name="Goals", value=stats["goals"], inline=True)
    embed.add_field(name="Assists", value=stats["assists"], inline=True)
    return embed

def embedded_team_stats(team_name, stats):
    """Build embedded message with team statistics"""
    return create_table(team_name, stats)
    # embed = discord.Embed(title=team_name, color=0xDC052D)
    # embed.set_thumbnail(url="https://clipartart.com/images/bavaria-logo-clipart.jpg")
    # embed.add_field(name="", value=info["height"], inline=True)
    # embed.add_field(name="Weight (kg)", value=info["weight"], inline=True)
    # embed.add_field(name="Position", value=info["position"], inline=True)
    # embed.add_field(name="Games Played", value=stats["gp"], inline=True)
    # embed.add_field(name="Goals", value=stats["goals"], inline=True)
    # embed.add_field(name="Assists", value=stats["assists"], inline=True)
    # return embed
