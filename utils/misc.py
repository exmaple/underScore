def umlaut(word):
    """Insert accented chars where applicable

    Args:
        word (str): a word containing an umlaut
    Returns:
        word with actual umlaut or just word
    """
    if "\\xc3\\xb6" in word:
        return word.replace("\\xc3\\xb6", "ö")
    elif "\\xc3\\xbc" in word:
        return word.replace("\\xc3\\xbc", "ü")
    else:
        return word


def get_author_info(ctx):
    return {
        "name": ctx.author.display_name,
        "icon_url": ctx.author.avatar_url,
    }