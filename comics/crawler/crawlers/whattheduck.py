from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'What the Duck'
    language = 'en'
    url = 'http://www.whattheduck.net/'
    start_date = '2006-07-01'
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Aaron Johnson'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed(
            'http://web.mac.com/aaronandpatty/'
            'What_the_Duck/Comic_Strips/rss.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.enclosures[0].type.startswith('image')
                and entry.title.startswith('WTD')):
                self.title = entry.title
                self.url = entry.enclosures[0].href
                return

    def update_titles(self):
        self.parse_feed(
            'http://web.mac.com/aaronandpatty/'
            'What_the_Duck/Comic_Strips/rss.xml')

        counter = 0
        for entry in self.feed.entries:
            split_title = entry.title.split(':')
            if len(split_title) > 1:
                try:
                    strip = self.comic.strip_set.filter(
                        title__startswith=split_title[0])[0]
                    if strip.title != entry.title:
                        strip.title = entry.title
                        strip.save()
                        counter += 1
                except IndexError:
                    pass
        return counter
