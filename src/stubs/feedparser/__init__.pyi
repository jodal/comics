from typing import IO, Any

class ThingsNobodyCaresAboutButMe(Exception): ...
class NonXMLContentType(ThingsNobodyCaresAboutButMe): ...

class FeedParserDict(dict[str, Any]):
    def __getattr__(self, name: str) -> Any: ...

def parse(
    url_file_stream_or_string: str | bytes | IO[Any],
    etag: str | None = None,
    modified: str | None = None,
    agent: str | None = None,
    referrer: str | None = None,
    handlers: Any = None,
    request_headers: Any = None,
    response_headers: Any = None,
    resolve_relative_uris: bool | None = None,
    sanitize_html: bool | None = None,
) -> FeedParserDict: ...
