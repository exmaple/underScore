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


def embed_dict(author_name, author_avatar, title, stats):
    embed = discord.Embed(title=title, color=0xDC052D)
    embed.set_author(name=author_name, icon_url=author_avatar)
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRWeGvePKW6vZ6kM5Wn6ZFqprk7lzoi73qd_MMlnoF46uIARNRA&usqp=CAU")

    for name, stat in stats.items():
        embed.add_field(name=name, value=stat, inline=False)

    return embed



def embedded_matchday_results(matchday, matches):
    """Build embedded message with matchday results

    Args:
        matchday (string): a number representing the matchday (eg. '2')
        matches (dict): dictionary containing team matchups and the corresponding score
            e.g. {0: [('Team Name 1', 'Score'),('Team Name 2', 'Score')], ... }

    Returns:
        embed message object
    """
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
