# memento-cli

[![Build Status](https://github.com/edsu/memento-cli/actions/workflows/test.yml/badge.svg)](https://github.com/edsu/memento-cli/actions/workflows/test.yml)

A command line tool interacting with Memento ([RFC 7089](https://www.rfc-editor.org/rfc/rfc7089)) supporting web archives, such as the Internet Archive's Wayback Machine.

## Usage

### List Snapshots

To list all the available snapshots (or Mementos) for a given snapshot you can use the `list` command:

```bash
$ memento list https://web.archive.org/web/20230407140923/https:/help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2017-12-29 05:40:51 https://web.archive.org/web/20171229054051/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-03 20:03:00 https://web.archive.org/web/20180103200300/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-04 06:39:58 https://web.archive.org/web/20180104063958/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-06 16:08:07 https://web.archive.org/web/20180106160807/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-12 06:10:07 https://web.archive.org/web/20180112061007/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-12 17:40:16 https://web.archive.org/web/20180112174016/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-12 18:40:34 https://web.archive.org/web/20180112184034/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-12 19:11:48 https://web.archive.org/web/20180112191148/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-20 19:05:57 https://web.archive.org/web/20180120190557/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
2018-01-20 19:19:20 https://web.archive.org/web/20180120191920/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
...
```

Since *memento* works with any RFC 7089 supporting archive you can use it to list versions in other web archives as well:

```bash
$ memento list https://www.webarchive.org.uk/wayback/archive/20130501020401/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition/
2013-05-01 02:03:57 https://www.webarchive.org.uk/wayback/archive/20130501020357mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition
2013-05-01 02:04:01 https://www.webarchive.org.uk/wayback/archive/20130501020401mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition/
2013-07-29 12:58:03 https://www.webarchive.org.uk/wayback/archive/20130729125803mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition
2013-07-29 12:58:06 https://www.webarchive.org.uk/wayback/archive/20130729125806mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition/
2021-01-22 06:38:21 https://www.webarchive.org.uk/wayback/archive/20210122063821mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition/
2022-03-14 16:36:16 https://www.webarchive.org.uk/wayback/archive/20220314163616mp_/http://www.vam.ac.uk/content/exhibitions/david-bowie-is/david-bowie-is-inside-the-exhibition/
```

### Searching for Changes (Bisect)

Let's suppose you know that the [Twitter Hateful Conduct Policy](https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy) used to have language about:

> women, people of color, lesbian, gay, bisexual, transgender, queer, intersex, asexual individuals
 
You can see it in the Internet Archive Wayback Machine [in 2019](https://web.archive.org/web/20190711134608/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy). But you can't see it [on the page in 2023](https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy). To identify when the change was introduced, you can *bisect* the version history to search for the version where the text went missing, using the two snapshots. This will perform a binary search between the two versions looking for the text.

```bash
$ memento bisect --missing --text "women, people of color, lesbian, gay" \
  https://web.archive.org/web/20190711134608/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy \
  https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
```

<img src="https://github.com/edsu/memento-cli/raw/main/images/memento.gif">

The *bisect* command uses a browser behind the scenes (using Selenium) in order to fully render the page. If you wanted to find out when some text appears (rather than goes missing) then remove the `--missing` parameter from the command.

And if you would prefer to examine the pages in between manually, leave off the `--text` parameter and *memento* will prompt you to continue, and show you the browser it is controlling.

If you would like to see the browser when using `--text` use the `--show-browser` option.
