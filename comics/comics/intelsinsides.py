from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "Intel's Insides"
    language = 'en'
    url = 'http://www.intelsinsides.com/'
    start_date = '2009-09-21'
    rights = 'Steve Lait'

class Crawler(CrawlerBase):
    history_capable_date = '2009-09-21'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/intelsinsides?format=xml')

	# There's no populated pubDate in the RSS feed; instead, the date is
	# listed in the title.  Sometimes, this date has a leading zero.
	# Sometimes, it does not.  So, we have to check both.
        base_date = pub_date.strftime('%d %B %Y')
        possible_dates = []
        possible_dates.append(base_date)
        if base_date[0] == '0':
            possible_dates.append(base_date[1:])

        for entry in feed.all():
            if entry.title not in possible_dates:
                continue
            url = entry.html(entry.description).src(
                'img[src*="images.nvidia.com"]')
            return CrawlerImage(url)
