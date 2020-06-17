import requests
import logging


logger = logging.getLogger("app")


def download_raw_html(url):
    """Download html page data

    Args:
        url (str): target url to download

    Returns:
        raw html string output
    """
    try:
        data = str(requests.get(url).content)

    except Exception:
        logger.debug(f"Unable to download file using param: {url}")

    return data
