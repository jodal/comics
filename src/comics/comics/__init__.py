from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING

from comics.aggregator.crawler import CrawlerBase

if TYPE_CHECKING:
    from types import ModuleType

    from comics.core.models import Comic


def get_comic_module_names() -> list[str]:
    module_names = [
        file.stem
        for file in Path(__file__).parent.glob("*.py")
        if not file.name.startswith("__init__")
    ]
    return sorted(module_names)


def get_comic_module(comic_slug: str) -> ModuleType:
    module_name = f"{__package__}.{comic_slug}"
    return importlib.import_module(module_name)


def get_comic_crawler(comic: Comic) -> CrawlerBase | None:
    module = get_comic_module(comic.slug)
    if not hasattr(module, "Crawler"):
        return None
    crawler = module.Crawler(comic)
    assert isinstance(crawler, CrawlerBase)
    return crawler
