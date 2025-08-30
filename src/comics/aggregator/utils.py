from __future__ import annotations

from typing import TYPE_CHECKING

from comics.comics import get_comic_module

if TYPE_CHECKING:
    from comics.core.models import Comic

SCHEDULE_DAYS = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]


def get_comic_schedule(comic: Comic):
    module = get_comic_module(comic.slug)
    schedule = module.Crawler(comic).schedule

    if not schedule:
        return []
    return [SCHEDULE_DAYS.index(day) for day in schedule.split(",")]
