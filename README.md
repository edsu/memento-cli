# memento-cli

A command line tool interacting with Memento supporting web archives, such as the Internet Archive's Wayback Machine.

## Usage

### List Snapshots

```bash
$ memento list https://web.archive.org/web/20230407140923/https:/help.twitter.com/en/rules-and-policies/hateful-conduct-policy
```

### Searching for Changes

Lets say you know that the [Twitter Hateful Conduct Policy](https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy) used to have language about "women, people of color, lesbian, gay, bisexual, transgender, queer, intersex, asexual individuals" because you can see it at the Internet Archive in 2019:

https://web.archive.org/web/20190711134608/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy

But you can see that it's not on the page in 2023:

https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy

If you want to identify when the change was introduced, you can *bisect* the page:

```bash
$ memento bisect https://web.archive.org/web/20190711134608/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
```

Which will do a binary search between the two points in the snapshots available in the archive to help you locate when the change occurred. Doing a binary search cuts down on the number of pages you will need to examine. You will be given URLs to look at and answer whether you see the change or not, and the tool will narrow the results until it finds the snapshot where the change was introduced.

In this case, since the phrase appears in the body of the page you can supply the text you want and mememnto will do the searching for you:

```bash
$ memento bisect --text "women, people of color, lesbian, gay" https://web.archive.org/web/20190711134608/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy https://web.archive.org/web/20230621094005/https://help.twitter.com/en/rules-and-policies/hateful-conduct-policy
```
