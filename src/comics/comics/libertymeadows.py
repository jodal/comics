from comics.aggregator.crawler import CreatorsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Liberty Meadows"
    language = "en"
    url = "http://www.creators.com/comics/liberty-meadows.html"
    start_date = "1997-03-30"
    end_date = "2001-12-31"
    rights = "Frank Cho"


class Crawler(CreatorsCrawlerBase):
    url_id = "153"
    history_capable_date = "2006-10-25"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Los_Angeles"
