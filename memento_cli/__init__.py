import click

from . import memento


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def list(url):
    # auto-detect the timemap if it's a memento supporting web archive
    timemap_url = memento.get_timemap_url(url)

    # if it's not a Memento URL construct a Wayback Machine timemap URL
    if timemap_url is None:
        timemap_url = f"https://web.archive.org/web/timemap/link/{url}"

    for mem in memento.get_mementos(timemap_url):
        print(mem.datetime, mem.url)


@cli.command()
@click.argument('start-url')
@click.argument('end-url')
@click.option('--text', help='text to search for on the page')
def bisect_urls(start_url, end_url, text):
    url = memento.bisect_urls(start_url, end_url, text)
    print(url)


def main():
    cli()
