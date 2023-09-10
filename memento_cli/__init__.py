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
@click.option('--text', help='text to look for on the page')
@click.option('--missing', is_flag=True, help='missing text to look for on the page')
@click.option('--show-browser', is_flag=True, help='see the browser')
def bisect(start_url, end_url, text, missing, show_browser):
    print()
    url = memento.bisect_urls(start_url, end_url, text, missing, show_browser)
    click.echo(f'\rFound your archive snapshot: {url}')


def main():
    cli()
