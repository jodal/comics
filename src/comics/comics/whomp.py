from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Whomp!"
    language = "en"
    url = "http://www.whompcomic.com/"
    start_date = "2010-06-14"
    rights = "Ronnie Filyaw"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    history_length_days = 70
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"
