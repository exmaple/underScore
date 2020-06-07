import discord


def dict_to_embed(d):
    if "title" in d.keys():
        embed = discord.Embed(title=d["title"], color=0xDC052D)

    if "name" in d.keys() and "icon_url" in d.keys():
        embed.set_author(name=d["name"], icon_url=d["icon_url"])

    # add if at some point
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRWeGvePKW6vZ6kM5Wn6ZFqprk7lzoi73qd_MMlnoF46uIARNRA&usqp=CAU")

    if "fields" in d.keys():
        for name, stat in d["fields"].items():
            embed.add_field(name=name, value=stat, inline=True)

    return embed
