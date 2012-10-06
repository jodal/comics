from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Greg Comic'
    language = 'en'
    url = 'http://gregcomic.com/'
    start_date = '2011-06-01'
    rights = 'Chur Yin Wan'

class Crawler(CrawlerBase):
    history_capable_date = '2011-06-01'
    schedule = 'Mo,We,Fr'
    time_zone = -5

    def crawl(self, pub_date):

        # First, pick up any posts on this date...
        page_url = 'http://gregcomic.com/%s' % \
            pub_date.strftime('%Y/%m/%d')
        page = self.parse_page(page_url)
        test_urls = page.href('td.archive-title a', allow_multiple=True)

        # ... then, comb posts looking for a comic (and not a blog entry)
        for test_url in test_urls:
            try:
                test_page = self.parse_page(test_url)
                url = test_page.src('div.comicpane img')
                title = test_page.alt('div.comicpane img')
                if url is not None:
                    return CrawlerImage(url, title)
            except StandardError:
                continue
