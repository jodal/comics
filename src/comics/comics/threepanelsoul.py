from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Three Panel Soul"
    language = "en"
    url = "http://www.threepanelsoul.com/"
    start_date = "2006-11-05"
    rights = "Ian McConville & Matt Boyd"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    history_capable_days = 180
    schedule = "Mo"
    time_zone = "America/New_York"
