# Creating crawlers

For each comic Comics is aggregating, we need to create a crawler. At the
time of writing, more than 200 crawlers are available in the
`src/comics/comics/` directory. They serve as a great source for learning how
to write new crawlers for Comics.

## A crawler example

The crawlers are split in two separate pieces. The `ComicData` part
contains meta data about the comic used for display at the web site. The
`Crawler` part contains properties needed for crawling and the crawler
implementation itself.

```python
from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'xkcd'
    language = 'en'
    url = 'https://www.xkcd.com/'
    start_date = '2005-05-29'
    rights = 'Randall Munroe, CC BY-NC 2.5'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('https://www.xkcd.com/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
```

## The `ComicData` class fields

- `name` -- _Required._ A string with the name of the comic.

- `language` -- _Required._ A two-letter string with the language code for
  the language used in the comic. Typically `'en'` or `'no'`.

    The language code must also be present in
    `comics.core.models.Comic.LANGUAGES`.

- `url` -- _Required._ A string with the URL of the comic's web page.

- `active` -- _Optional._ Whether or not this comic is still being crawled.
  Defaults to `True`.

- `start_date` -- _Optional._ The first date the comic was published at.

- `end_date` -- _Optional._ The last date the comic was published at if it
  is discontinued.

- `rights` -- _Optional._ Name of the author and the comic's license if
  available.

## The `Crawler` class fields

- `history_capable_date` -- _Optional._ Date of oldest release available for
  crawling.

    Provide this _or_ `history_capable_days`. If both are present, this one
    will have precedence.

    Example: `'2008-03-08'`.

- `history_capable_days` -- _Optional._ Number of days a release is
  available for crawling.

    Provide this _or_ `history_capable_date`.

    Example: `32`.

- `schedule` -- _Optional._ On what weekdays the comic is published.

    Example: `'Mo,We,Fr'` or `'Mo,Tu,We,Th,Fr,Sa,Su'`.

- `time_zone` -- _Optional._ In approximately what time zone the comic is
  published.

    Example: `Europe/Oslo` or `US/Eastern`.

    See [the IANA timezone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    for a list of possible values.

- `multiple_releases_per_day` -- _Optional._ Default: `False`. Whether to
  allow multiple releases per day.

    Example: `True` or `False`.

- `has_rerun_releases` -- _Optional._ Default: `False`. Whether the comic
  reruns old images as new releases.

    Example: `True` or `False`.

- `headers` -- _Optional._ Default: `None`. Any HTTP headers to send with
  any URI request for values.

    Useful if you're pulling comics from a site that checks either the
    `Referer` or `User-Agent`. If you can view the comic using your browser
    but not when using your loader for identical URLs, try setting the
    `Referer` to be `http://www.example.com/` or set the `User-Agent` to be
    `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)`.

    Example:
    `{'Referer': 'http://www.example.com/', 'Host': 'http://www.example.com/'}`

## The `Crawler.crawl()` method

The `Crawler.crawl()` is where the real work is going on. To start with
an example, let's look at _XKCD_'s `Crawler.crawl()` method:

```python
def crawl(self, pub_date):
    feed = self.parse_feed('http://www.xkcd.com/rss.xml')
    for entry in feed.for_date(pub_date):
        url = entry.summary.src('img[src*="/comics/"]')
        title = entry.title
        text = entry.summary.alt('img[src*="/comics/"]')
        return CrawlerImage(url, title, text)
```

### Arguments and return values

The `Crawler.crawl()` method takes a single argument, `pub_date`, which
is a `datetime.date` object for the date the crawler is currently
crawling. The goal of the method is to return a `CrawlerImage` object
containing at least the URL of the image for `pub_date` and optionally a
`title` and `text` accompanying the image. `CrawlerImage`'s signature is:

```python
CrawlerImage(url, title=None, text=None)
```

This means that you must always supply an URL, and that you can supply a
`text` without a `title`. The following are all valid ways to create a
`CrawlerImage`:

```python
CrawlerImage(url)
CrawlerImage(url, title)
CrawlerImage(url, title, text)
CrawlerImage(url, text=text)
```

For some crawlers, this is all you need. If the image URL is predictable and
based upon the `pub_date` in some way, just create the URL with the help of
[Python's strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior),
and return it wrapped in a `CrawlerImage`:

```python
def crawl(self, pub_date):
    url = 'http://www.example.com/comics/%s.png' % (
        pub_date.strftime('%Y-%m-%d'),
    )
    return CrawlerImage(url)
```

Though, for most crawlers, some interaction with RSS or Atom feeds or web
pages are needed. For this a
[web parser](#parsing-web-pages-with-lxmlparser) and a
[feed parser](#parsing-feeds-with-feedparser) are provided.

### Returning multiple images for a single comic release

Some comics got releases with multiple images, and thus returning a single
`CrawlerImage` will not be enough for you. For situations like these,
Comics lets you return a list of `CrawlerImage` objects from
`Crawler.crawl()`. The list should be ordered in the same way as the
comic is meant to be read, with the first frame as the first element in the
list. If the comic release got a `title`, add it to the first
`CrawlerImage` object, and let the `title` field stay empty on the
rest of the list elements. The same applies for the `text` field, unless each
image actually got a different `title` or `text` string.

The following is an example of a `Crawler.crawl()` method which returns
multiple images. It adds a `title` to the first list element, and different
`text` to all of the elements.

```python
def crawl(self, pub_date):
    feed = self.parse_feed('http://feeds.feedburner.com/Pidjin')
    for entry in feed.for_date(pub_date):
        result = []
        for i in range(1, 10):
            url = entry.content0.src('img[src$="000%d.jpg"]' % i)
            text = entry.content0.title('img[src$="000%d.jpg"]' % i)
            if url and text:
                result.append(CrawlerImage(url, text=text))
        if result:
            result[0].title = entry.title
        return result
```

## Parsing web pages with `LxmlParser`

The web parser, internally known as `LxmlParser`, uses CSS selectors to
extract content from HTML. For a primer on CSS selectors, see
[Matching HTML elements using CSS selectors](#matching-html-elements-using-css-selectors).

The web parser is accessed through the `Crawler.parse_page` method:

```python
def crawl(self, pub_date):
    page_url = 'http://ars.userfriendly.org/cartoons/?id=%s' % (
        pub_date.strftime('%Y%m%d'),)
    page = self.parse_page(page_url)
    url = page.src('img[alt^="Strip for"]')
    return CrawlerImage(url)
```

This is a common pattern for crawlers. Another common patterns is to use a
feed to find the web page URL for the given date, then parse that web page to
find the image URL.

### `LxmlParser` API

The available methods only require a CSS selector, `selector`, to match tags.
In the event that the selector doesn't match any elements, `default` will be
returned.

If the `selector` matches multiple elements, one of two things will happen:

- For singular methods, a `MultipleElementsReturned` exception is raised.
- For plural methods, a list of zero or more values are returned.

Methods on `LxmlParser`:

- `text(selector, default=None)` -- Returns the text contained by the
  element matching `selector`.

- `texts(selector)` -- Returns a list of the text contained by the elements
  matching `selector`.

- `src(selector, default=None)` -- Returns the `src` attribute of the
  element matching `selector`.

    The web parser automatically expands relative URLs in the source, like
    `/comics/2008-04-13.png` to a full URL like
    `http://www.example.com/2008-04-13.png`, so you do not need to think
    about that.

- `srcs(selector)` -- Returns the `src` attribute of the elements matching
  `selector`.

- `alt(selector, default=None)` -- Returns the `alt` attribute of the
  element matching `selector`.

- `alts(selector)` -- Returns the `alt` attribute of the elements matching
  `selector`.

- `title(selector, default=None)` -- Returns the `title` attribute of the
  element matching `selector`.

- `titles(selector)` -- Returns the `title` attribute of the elements
  matching `selector`.

- `href(selector, default=None)` -- Returns the `href` attribute of the
  element matching `selector`.

- `hrefs(selector)` -- Returns the `href` attribute of the elements matching
  `selector`.

- `value(selector, default=None)` -- Returns the `value` attribute of the
  element matching `selector`.

- `values(selector, default=None)` -- Returns the `value` attribute of the
  elements matching `selector`.

- `id(selector, default=None)` -- Returns the `id` attribute of the element
  matching `selector`.

- `ids(selector, default=None)` -- Returns the `id` attribute of the
  elements matching `selector`.

- `remove(selector)` -- Remove the elements matching `selector` from the
  parsed document.

### Matching HTML elements using CSS selectors

Both web page and feed parsing uses CSS selectors to extract the interesting
strings from HTML. CSS selectors are those normally simple strings you use in
CSS style sheets to select what elements of your web page the CSS declarations
should be applied to.

In the following example `h1 a` is the selector. It matches all `a`
elements contained in `h1` elements. The rule to be applied to the matching
elements is `color: red;`.

```css
h1 a { color: red; }
```

Similarly `class="foo"` and `id="bar"` in HTML may be used in CSS
selectors. The following CSS example would color all `h1` headers with the
class `foo` red, and all elements with the ID `bar` which is contained in
`h1` elements would be colored blue.

```css
h1.foo { color: red; }
h1 #bar { color: blue; }
```

In CSS3, the power of CSS selectors have been greatly increased by the
addition of matching by the content of elements' attributes. To match all
`img` elements with a `src` attribute _starting with_
`http://www.example.com/` simply write:

```css
img[src^="http://www.example.com/"]
```

Or, to match all `img` elements whose `src` attribute _ends in_ `.jpg`:

```css
img[src$=".jpg"]
```

Or, `img` elements whose `src` attribute _contains_ `/comics/`:

```css
img[src*="/comics/"]
```

Or, `img` elements whose `alt` attribute _is_ `Today's comic`:

```css
img[alt="Today's comic"]
```

For further details on CSS selectors in general, please refer to
<http://css.maxdesign.com.au/selectutorial/>.

## Parsing feeds with `FeedParser`

The feed parser is initialized with a feed URL passed to
`Crawler.parse_feed`, just like the web parser is initialized with a web
page URL:

```python
def crawl(pub_date):
    ...
    feed = self.parse_feed('http://www.xkcd.com/rss.xml')
    ...
```

### `FeedParser` API

The `feed` object provides two methods which both returns feed elements:
`FeedParser.for_date` and `FeedParser.all`. Typically, a crawler
uses `FeedParser.for_date` and loops over all entries it returns to find
the image URL:

```python
for entry in feed.for_date(pub_date):
    # parsing comes here
    return CrawlerImage(url)
```

Methods on `FeedParser`:

- `for_date(date)` -- Returns all feed elements published at `date`.

- `all()` -- Returns all feed elements.

### Feed `Entry` API

The Comics feed parser is really a combination of the popular
[feedparser](https://github.com/kurtmckee/feedparser) library and
`LxmlParser`. It can do anything _feedparser_ can do, and in addition you can
use the `LxmlParser` methods on feed fields which contains HTML, like
`Entry.summary` and `Entry.content0`.

Fields and methods on `Entry`:

- `summary` -- This is the most frequently used entry field which supports
  HTML parsing with the `LxmlParser` methods.

    Example usage:

    ```python
    url = entry.summary.src('img')
    title = entry.summary.alt('img')
    ```

- `content0` -- This is the same as _feedparser_'s `content[0].value`
  field, but with `LxmlParser` methods available. For some crawlers, this is
  where the interesting stuff is found.

- `html(string)` -- Wrap `string` in a `LxmlParser`.

    If you need to parse HTML in any other fields than `summary` and
    `content0`, you can apply the `html(string)` method on the field, like
    it is applied on a feed entry's title field here:

    ```python
    title = entry.html(entry.title).text('h1')
    ```

- `tags` -- List of tags associated with the entry.

## Testing your new crawler

When the first version of you crawler is complete, it's time to test it.

The file name is important, as it is used as the comic's slug. This means that
it must be unique within the Comics installation, and that it is used in the
URLs Comics will serve the comic at. For this example, we call the crawler
file `foo.py`. The file must be placed in the `src/comics/comics/`
directory, and will be available in Python as `comics.comics.foo`.

### Loading `ComicData` for your new comic

For Comics to know about your new crawler, you need to load the comic meta
data into Comics' database. To do so, we run the `add_comics` command:

```sh
uv run comics add_comics -c foo
```

If you do any changes to the `ComicData` class of any crawler, you must
rerun `add_comics` to update the database representation of the comic.

### Running the crawler

When `add_comics` has created a `comics.core.models.Comic` instance for the
new crawler, you may use your new crawler to fetch the comic's release for the
current date by running:

```sh
uv run comics get_releases -c foo
```

If you want to get comics releases for more than the current day, you may
specify a date range to crawl, like:

```sh
uv run comics get_releases -c foo -f 2009-01-01 -t 2009-03-31
```

The date range will automatically be adjusted to the crawlers _history
capability_. You may also get comics for a date range without a specific end.
In which case, the current date will be used instead:

```sh
uv run comics get_releases -c foo -f 2009-01-01
```

If your new crawler is not working properly, you may add `-v2` to the command
to turn on full debug output:

```sh
uv run comics get_releases -c foo -v2
```

For a full overview of `get_releases` options, run:

```sh
uv run comics get_releases --help
```

## Submitting your new crawler for inclusion in Comics

When your crawler is working properly, you may submit it for inclusion in
Comics. You should fork Comics at
[GitHub](https://github.com/jodal/comics), commit your new crawler to your
own fork, and send me a _pull request_ through GitHub.

All contributions must be granted under the same license as Comics itself.
