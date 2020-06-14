def umlaut(word_with_umlaut):
    """Insert accented chars where applicable

    Args:
        word_with_umlaut(str): a word containing an umlaut
    Returns:
        word with actual umlaut
    """
    if "\\xc3\\xb6" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xb6", "ö")
    if "\\xc3\\xbc" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xbc", "ü")
    if "\\" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\", "")
    return word_with_umlaut
