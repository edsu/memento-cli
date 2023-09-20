import re
import shutil
import datetime
import requests
import requests.utils

from collections import namedtuple

from .browser import Browser


Memento = namedtuple("Memento", ["url", "datetime"])


def get_timemap_url(url):
    """
    Look for a Memento Timemap URL in the response headers for a web resource.
    """
    resp = requests.get(url)
    if (
        resp.status_code == 200
        and "timemap" in resp.links
        and "url" in resp.links["timemap"]
    ):
        return resp.links["timemap"]["url"]
    return None


def get_mementos(timemap_url) -> list[Memento]:
    """
    Fetches a Memento Timemap URL and returns it as a list of Links.
    """
    resp = requests.get(timemap_url)
    mementos = []
    if resp.headers.get("content-type") == "application/link-format":
        for link in parse_links(resp.text):
            if link.get("rel") == "memento":
                mementos.append(
                    Memento(
                        link["url"],
                        datetime.datetime.strptime(
                            link["datetime"], "%a, %d %b %Y %H:%M:%S GMT"
                        ),
                    )
                )

    return mementos


def parse_links(text) -> list[dict]:
    """
    Return a list of dictionaries for RFC 6690 header links.
    """
    # lean on requests for the parsing, but make prep the text to allow for
    # whitespace since parse_header_links is designed for a single line header

    text = re.sub(r"^\s+", "", text)  # strip leading whitespace
    text = re.sub(
        r",\s*$", "", text
    )  # strip trailing comma and any optional whitespace
    text = re.sub(r'",\r?\n', ", ", text)  # remove dos/unix newlines between links

    return requests.utils.parse_header_links(text)


def bisect_urls(
    start_url, end_url=None, text=None, missing=False, show_browser=False
) -> str:
    timemap_url = get_timemap_url(start_url)
    mementos = sorted(get_mementos(timemap_url), key=lambda m: m.datetime)
    memento_urls = [m.url for m in mementos]

    start = memento_urls.index(start_url)
    end = memento_urls.index(end_url) if end_url else len(memento_urls) - 1

    if text is None:
        show_browser = True

    browser = Browser(headless=(not show_browser))

    return bisect(start, end, memento_urls, text, missing, browser)


def bisect(start, end, memento_urls, text, missing, browser) -> str:
    mid = start + int((end - start) / 2)
    if mid == start:
        return memento_urls[end]

    page_text = browser.get(memento_urls[mid])

    # if user wants to look at the page themselves
    if text is None:
        answer = input("Do you see the change? [y/n] ")
        if answer.lower() == "y":
            text_in_page = True
        else:
            text_in_page = False
    # look in the page text
    else:
        print("\r" + meter(start, end, len(memento_urls)), end="")
        text_in_page = bool(re.search(text, page_text))

    # do we want to find the page where the text went missing?
    if missing:
        if not text_in_page:
            return bisect(start, mid, memento_urls, text, missing, browser)
        else:
            return bisect(mid, end, memento_urls, text, missing, browser)

    # or do we want to find the page where the text started appearing?
    else:
        if text_in_page:
            return bisect(start, mid, memento_urls, text, missing, browser)
        else:
            return bisect(mid, end, memento_urls, text, missing, browser)


def meter(start, end, n):
    # get the width of the progress bar (factoring in the leading counter)
    width = shutil.get_terminal_size().columns - (len(str(n)) * 2 + 10)
    scale = width / n
    a = int((start + 1) * scale)
    b = int((end - start + 1) * scale)
    c = int((n - end + 1) * scale)

    return f"[{n - (end - start)}/{n}]: " + a * "█" + b * "░" + c * "█"
