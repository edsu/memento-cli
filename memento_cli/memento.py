import re
import datetime
import requests
import requests.utils

from collections import namedtuple

from .browser import Browser


Memento = namedtuple('Memento', ['url', 'datetime'])

def get_timemap_url(url):
    """
    Look for a Memento Timemap URL in the response headers for a web resource.
    """
    resp = requests.get(url)
    if resp.status_code == 200 and 'timemap' in resp.links and 'url' in resp.links['timemap']:
        return resp.links['timemap']['url']
    return None


def get_mementos(timemap_url) -> list[Memento]:
    """
    Fetches a Memento Timemap URL and returns it as a list of Links.
    """
    resp = requests.get(timemap_url)
    mementos = []
    if resp.headers.get('content-type') == 'application/link-format':
        for link in parse_links(resp.text):
            if link.get('rel') == 'memento':
                mementos.append(Memento(
                    link['url'],
                    datetime.datetime.strptime(link['datetime'], "%a, %d %b %Y %H:%M:%S GMT")
                ))
    
    return mementos


def parse_links(text) -> list[dict]:
    """
    Return a list of dictionaries for RFC 6690 header links.
    """
    # lean on requests for the parsing, but make prep the text to allow for
    # whitespace since parse_header_links is designed for a single line header

    text = re.sub(r'^\s+', '', text)        # strip leading whitespace
    text = re.sub(r',\s*$', '', text)       # strip trailing comma and any optional whitespace
    text = re.sub(r'",\r?\n', ', ', text)   # remove dos/unix newlines between links

    return requests.utils.parse_header_links(text)


def bisect_urls(start_url, end_url, text) -> str:
    timemap_url = get_timemap_url(start_url)
    mementos = sorted(get_mementos(timemap_url), key=lambda m: m.datetime)
    memento_urls = [m.url for m in mementos]

    start = memento_urls.index(start_url)
    end = memento_urls.index(end_url)

    return bisect(start, end, memento_urls, text)


def bisect(start, end, memento_urls, text, browser=None) -> str: 
    print(start, end)
    if browser == None:
        browser = Browser(headless=True)

    mid = start + int((end - start) / 2)
    if mid == start:
        return memento_urls[end]

    page_text = browser.get(memento_urls[mid])
    if text in page_text:
        return bisect(start, mid, memento_urls, text, browser)
    else:
        return bisect(mid, end, memento_urls, text, browser)
