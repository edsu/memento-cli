import datetime

from memento_cli.memento import (
    get_timemap_url,
    get_mementos,
    parse_links,
    bisect,
    bisect_urls,
)

from memento_cli.browser import Browser


def test_get_timemap_url():
    assert (
        get_timemap_url(
            "https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy"
        )
        == "https://web.archive.org/web/timemap/link/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy"
    )
    assert (
        get_timemap_url("https://perma.cc/7CN8-NJNV")
        == "https://perma.cc/timemap/html/http://arboretum.harvard.edu"
    )
    assert (
        get_timemap_url(
            "https://swap.stanford.edu/was/20230524140954/http://news.stanford.edu/"
        )
        == "https://swap.stanford.edu/was/timemap/link/http://news.stanford.edu/"
    )
    assert get_timemap_url("https://nytimes.com") is None


def test_get_mementos():
    mementos = list(
        get_mementos(
            "https://web.archive.org/web/timemap/link/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy"
        )
    )
    assert len(mementos) > 2000
    assert (
        mementos[0].url
        == "https://web.archive.org/web/20171229054051/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy"
    )
    assert mementos[0].datetime == datetime.datetime(2017, 12, 29, 5, 40, 51)
    assert mementos[-1].datetime.year >= 2023


def test_parse_links():
    text = """
<http://www.nytimes.com:80/>; rel="original",
<https://web.archive.org/web/timemap/link/https://nytimes.com/>; rel="self"; type="application/link-format"; from="Tue, 12 Nov 1996 18:15:13 GMT",
<https://web.archive.org/web/https://nytimes.com/>; rel="timegate",
<https://web.archive.org/web/19961112181513/http://www.nytimes.com:80/>; rel="first memento"; datetime="Tue, 12 Nov 1996 18:15:13 GMT",
<https://web.archive.org/web/19961112181513/http://www.nytimes.com:80/>; rel="memento"; datetime="Tue, 12 Nov 1996 18:15:13 GMT",
<https://web.archive.org/web/19961112181513/http://www.nytimes.com:80/>; rel="memento"; datetime="Tue, 12 Nov 1996 18:15:13 GMT",
<https://web.archive.org/web/19961121230155/http://www.nytimes.com:80/>; rel="memento"; datetime="Thu, 21 Nov 1996 23:01:55 GMT",
<https://web.archive.org/web/19961219002950/http://www.nytimes.com:80/>; rel="memento"; datetime="Thu, 19 Dec 1996 00:29:50 GMT",
    """
    links = parse_links(text)
    assert len(links) == 8
    assert links[0]["rel"] == "original"
    assert links[0]["url"] == "http://www.nytimes.com:80/"
    assert (
        links[7]["url"]
        == "https://web.archive.org/web/19961219002950/http://www.nytimes.com:80/"
    )
    assert links[7]["rel"] == "memento"
    assert links[7]["datetime"] == "Thu, 19 Dec 1996 00:29:50 GMT"


def test_bisect_urls():
    start_url = "http://web.archive.org/web/20200102102511/https://inkdroid.org/"
    end_url = "http://web.archive.org/web/20230902020134/https://inkdroid.org/"

    url = bisect_urls(start_url, end_url, "ReSpec Writing")
    assert url == "http://web.archive.org/web/20230601013229/https://inkdroid.org/"


def test_bisect():
    timemap = get_timemap_url(
        "http://web.archive.org/web/20230902020134/https://inkdroid.org/"
    )
    mementos = sorted(get_mementos(timemap), key=lambda m: m.datetime)
    mementos = [m.url for m in mementos]
    browser = Browser(headless=True)

    url = bisect(
        0, len(mementos), mementos, "ReSpec Writing", missing=False, browser=browser
    )
    assert url == "http://web.archive.org/web/20230601013229/https://inkdroid.org/"

def test_bisect_regex():
    start_url = "http://web.archive.org/web/20200102102511/https://inkdroid.org/"
    end_url = "http://web.archive.org/web/20230902020134/https://inkdroid.org/"

    url = bisect_urls(start_url, end_url, "ReSpe. Writing")
    assert url == "http://web.archive.org/web/20230601013229/https://inkdroid.org/"

def test_browser():
    browser = Browser(headless=True)
    text = browser.get(
        "https://swap.stanford.edu/was/20230524140954/https://library.stanford.edu/node/172367"
    )
    # This text appears in an iframe provided by pywb
    assert "East Asian telegraph codes" in text
