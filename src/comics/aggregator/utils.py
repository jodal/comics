from __future__ import annotations

from typing import TYPE_CHECKING

from comics.comics import get_comic_crawler

if TYPE_CHECKING:
    from comics.core.models import Comic

SCHEDULE_DAYS = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]


def get_comic_schedule(comic: Comic) -> list[int]:
    crawler = get_comic_crawler(comic)
    if crawler is None or not crawler.schedule:
        return []
    return [SCHEDULE_DAYS.index(day) for day in crawler.schedule.split(",")]
