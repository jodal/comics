from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Ménage à 3"
    language = "en"
    url = "http://www.ma3comic.com/"
    start_date = "2008-05-17"
    rights = "Giz & Dave Zero 1"
    active = False


class Crawler(ComicControlCrawlerBase):
    base_url = "https://pixietrixcomix.com/menage-a-3"
    history_length_days = 50
    schedule = "Tu,Th,Sa"
    time_zone = "America/New_York"
