# Repairing a broken crawler

A crawler is broken when the site still publishes the comic, but the crawler
no longer finds the releases. Follow this routine for each broken crawler.

Give every crawler the same checks. The age of the last release does not
change the routine. A crawler that fetched nothing for seven years can be as
easy to repair as one that broke last month.

Do not assume. Every conclusion in this routine needs evidence that you
collected in this session.

## Stop points

Make the change yourself only when a real fetch proves that the crawler works
again. Stop and ask the user before you do any of these:

- Retire a comic.
- Use a new domain or a new site that you found by search. A redirect
  from the comic's own old address is not such a find: follow it.
- Report a comic as published but not crawlable.

At a stop point, show the evidence you collected, name the action you
recommend, and wait.

## Step 1: Select the comics

The routine accepts two kinds of input.

**A saved status page.** The site publishes a crawler status page at
`/status/`. Save it and pass the file. The page holds one table with
`id="status"`. Each row holds:

- A link with the comic's slug.
- A link to the comic's site.
- The number of days since the last release, for example `2753d`.
- One cell per day. The cell class is `scheduled`, `fetched`, both, or empty.

Read the days since the last release together with the crawler's `schedule`
attribute. A low number of `fetched` cells is not proof of a fault on its
own, because a comic without a `schedule` is scheduled every day, and an
irregular comic then looks the same as a broken one.

**A list of slugs.** The user names the comics. Do not triage. Run the
per-comic steps on each named comic.

## Step 2: Reproduce the fault

The comic must be in the local development database:

```sh
uv run comics add_comics -c <slug>
```

Crawl today, and then a range of recent days:

```sh
uv run comics get_releases -c <slug>
uv run comics get_releases -c <slug> -f <YYYY-MM-DD> -t <YYYY-MM-DD>
```

The command writes to the local database and to `run/media/`. This has no
effect on the production instance.

`No release found` does not tell you why. It means both "the site published
nothing" and "the crawler found nothing in what the site sent". Step 3 finds
out which.

## Step 3: Probe the source

Read the crawler module first. Note each URL it requests, and each selector
it applies.

Then request the same URLs yourself:

```sh
dig +short <domain>                            # Does the domain resolve?
curl -sSI -A "Mozilla/5.0" <url>               # Status, redirects, content type
curl -sS -A "Mozilla/5.0" <url> | head -c 4000 # Body, feed or page
```

Answer these questions, and write down the evidence for each answer:

1. Does the domain resolve?
2. Does the site answer, and with which status code?
3. Where does a redirect send you?
4. Does the feed or the page still exist at the URL the crawler uses?
5. Does the site still publish new releases? Find the date of the most recent
   release on the site.
6. Do the crawler's selectors still match what the site sends?

## Step 4: Search for a move

A comic that is absent from its old address is not always finished. Comics
move to new domains, and to platforms such as GoComics, Comics Kingdom,
Webtoon, Tumblr, Substack, or Patreon.

Search for the comic's name, for the author's name, and for a phrase from the
comic's site. Look at the author's public profiles for a link to the current
site.

If the comic's old address redirects to the new one, the source itself
says where the comic moved. Follow the redirect and repair the crawler. The
same holds when the old feed or page names the new address.

The user must approve every site that only a search connects to the comic.
Before you ask, confirm that:

- The new site holds the same comic, and not a different work by the same
  author.
- The new site publishes new releases.
- The releases carry a date, or the site otherwise lets a crawler select the
  release for one date.

Report what you found, and where you found it. Then stop.

## Step 5: Classify the fault

| Observation | Cause | Treatment |
| --- | --- | --- |
| The domain does not resolve | The site is gone | Search for a move, then retire |
| TLS or certificate error | The site is abandoned | Search for a move, then retire |
| HTTP 403 or 429 | The site refuses the request | Set `headers` |
| HTTP 404 on the feed | The feed moved or was removed | Find the new feed, or crawl the page |
| Redirect to a parked page or a social profile | The comic left the site | Search for a move, then retire |
| HTTP 200, but no selector matches | The markup changed | Update the selectors |
| The feed holds entries, but none for the date | Wrong `schedule` or `time_zone`, or the comic is on hiatus | Correct the attribute, or leave the comic alone |
| The site publishes only through JavaScript | The crawler cannot read the page | Stop and ask |
| Many comics on one host fail together | A shared crawler base broke | Repair the base class |

These bases in `src/comics/aggregator/crawler.py` serve many comics. Repair
the base, not each comic:

- `GoComicsCrawlerBase`
- `ComicsKingdomCrawlerBase`
- `CreatorsCrawlerBase`
- `ComicControlCrawlerBase`

## Step 6: Repair the crawler

Change the crawler module. Keep the change as small as the fault needs.

Use the tools that the crawler base gives you: `parse_feed()`, `parse_page()`,
`string_to_date()`, and the `headers` attribute. `LxmlParser` selects with CSS
selectors and reads attributes with `src()`, `href()`, `alt()`, `title()`,
`text()`, and `attr()`, each with a plural form that returns a list.

If the site refuses the request, set a header on the crawler:

```python
class Crawler(CrawlerBase):
    headers = {"User-Agent": "Mozilla/5.0"}
```

Some sites need a `Referer` header instead.

## Step 7: Verify the repair

Crawl a range of recent days on which the comic published:

```sh
uv run comics get_releases -c <slug> -f <YYYY-MM-DD> -t <YYYY-MM-DD>
```

The repair is proved only when the command fetches a real release. Keep the
range small. Do not crawl the full history to fill the gap: the local database
is not the production instance, so a backfill here has no value.

Then run the checks:

```sh
ruff format .
ruff check .
basedpyright src
```

## Step 8: Retire a comic

Retire a comic only after the user approves it.

Find the date on which the source published the comic for the last time. Use
the site itself, or an archive such as `web.archive.org`. Do not use the date
of the last release in the database: the crawler often broke long before the
comic ended.

Set the metadata, and delete the whole `Crawler` class and the imports that
become unused:

```python
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Example Comic"
    language = "en"
    url = "http://www.example.com/"
    start_date = "2005-05-29"
    end_date = "2019-11-14"
    active = False
    rights = "A. Author"
```

If the comic still publishes, but no crawler can read the site, do not retire
it. Stop and ask.

## Step 9: Commit

Change only one crawler in each commit. Name the comic by its slug, not by
its name:

```text
fix: Update examplecomic crawler after site change
```

Give the evidence for a retirement in the body:

```text
chore: Retire examplecomic

The site still answers, but the last comic is from 2019-11-14.
```

Put a change to a shared crawler base, to the aggregator, or to any other
file that serves every comic in its own commit, before the crawler commits.
