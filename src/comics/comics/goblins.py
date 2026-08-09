from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Goblins"
    language = "en"
    url = "http://www.goblinscomic.com/"
    start_date = "2005-05-29"
    rights = "Tarol Hunt"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    history_capable_days = 30
    time_zone = "America/Los_Angeles"
