from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Sticky Dilly Buns"
    language = "en"
    url = "http://www.stickydillybuns.com/"
    start_date = "2013-01-07"
    rights = "G. Lagace"
    active = False


class Crawler(ComicControlCrawlerBase):
    base_url = "https://pixietrixcomix.com/sticky-dilly-buns"
    history_length_days = 50
    schedule = "Mo,Fr"
    time_zone = "America/New_York"
