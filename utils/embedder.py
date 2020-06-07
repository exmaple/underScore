import discord

def dict_to_embed(author_name, author_avatar, title, stats):
    embed = discord.Embed(title=title, color=0xDC052D)
    embed.set_author(name=author_name, icon_url=author_avatar)
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRWeGvePKW6vZ6kM5Wn6ZFqprk7lzoi73qd_MMlnoF46uIARNRA&usqp=CAU")

    for name, stat in stats.items():
        embed.add_field(name=name, value=stat, inline=True)

    return embed
