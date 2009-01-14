from comics.crawler.crawlers import BaseComicsComComicCrawler

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Pearls Before Swine')
