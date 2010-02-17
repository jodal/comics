import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Joe Loves Crappy Movies'
    language = 'en'
    url = 'http://www.digitalpimponline.com/strips.php?title=movie'
    start_date = '2005-04-04'
    rights = 'Joseph Dunn'

class Crawler(CrawlerBase):
    history_capable_date = '2005-04-04'
    # It's updated quite irregularly, actually... ignore that schedule
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    # This crawler is pretty complicated because this dude does everything by
    # ID with only a loose date-mapping and re-using names (which you're not
    # allowed to do in HTML, but he's an ass like that)
    def crawl(self, pub_date):
        date_to_index_page = self.parse_page(
            'http://www.digitalpimponline.com/strips.php?title=movie')

        # Go through all IDs in the document, checking to see if the date is
        # the date we want in the option drop-down
        possible_ids = date_to_index_page.value('select[name="id"] option',
            allow_multiple=True)
        the_id = None

        # (cheap conversion to a set to eliminate the duplicate IDs from
        # different parts of the HTML to save time...)
        for possible_id in set(possible_ids):
            # We're going to get two results back.  One is the potential date,
            # the other is the title.  I can't think of a good way to enforce
            # that we get the real value first, then the title, so we're just
            # going to parse it again later.
            possible_date_and_title = date_to_index_page.text('option[value=%s]'
                % possible_id, allow_multiple=True)
            for the_date in possible_date_and_title:
                # Make sure we strip off the leading '0' on %d: Joe doesn't
                # include them.  We can't use a regex due to the speed
                # penalty of ~500+ regex comparisons
                    if the_date == pub_date.strftime(r"%B %d, %Y").replace(
                            " 0", " ", 1):
                        the_id = possible_id
                        break

        # Make sure we got an ID...
        if the_id is None:
            return

        # We got an ID:  Now, pull that page...
        right_page = self.parse_page(
            'http://www.digitalpimponline.com/strips.php?title=movie&id=%s' % 
            the_id)

        # ...and parse the url...
        # (the URL has a leading ../, when it's in the base directory already.
        # Work around the glitch)
        url = right_page.src('img[class=strip]').replace("../", "")
        title = None

        # ... go through some rigamarole to get the title of the comic being
        # reviewed...  Basically, the selects for the date and movie title are
        # identical in basically every way.  We have to therefore get the
        # selected ones.  One is the date.  One is the title.  Check for the
        # date.
        possible_titles = right_page.text('select[name="id"] option[selected]',
            allow_multiple=True)

        for possible_title in possible_titles:
            if pub_date.strftime("%Y") in possible_title:
                continue
            else:
                title = possible_title

        return CrawlerImage(url, title=title)
