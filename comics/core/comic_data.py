import logging
from dataclasses import dataclass, field
from typing import List, Optional, TypedDict

from comics.comics import get_comic_module, get_comic_module_names
from comics.core.exceptions import ComicDataError
from comics.core.models import Comic

logger = logging.getLogger("comics.core.comic_data")


class Options(TypedDict):
    comic_slugs: List[str]


@dataclass
class ComicDataBase:
    # Required values
    language: str = field(init=False)
    slug: str = field(init=False)
    name: str = field(init=False)
    url: str = field(init=False)

    # Default values
    active: bool = field(init=False, default=True)
    start_date: Optional[str] = field(init=False, default=None)
    end_date: Optional[str] = field(init=False, default=None)
    rights: str = field(init=False, default="")

    def __post_init__(self) -> None:
        self.slug = self.__module__.split(".")[-1]


class ComicDataLoader:
    def __init__(self, options: Options) -> None:
        self.include_inactive = self._get_include_inactive(options)
        self.comic_slugs = self._get_comic_slugs(options)

    def start(self) -> None:
        for comic_slug in self.comic_slugs:
            logger.info("Loading comic data for %s", comic_slug)
            self._try_load_comic_data(comic_slug)

    def stop(self) -> None:
        pass

    def _get_include_inactive(self, options: Options) -> bool:
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug("Excluding inactive comics")
            return False
        else:
            logger.debug("Including inactive comics")
            return True

    def _get_comic_slugs(self, options: Options) -> List[str]:
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.error("No comic given. Use -c option to specify comic(s).")
            return []
        elif "all" in comic_slugs:
            logger.debug("Load targets: all comics")
            return get_comic_module_names()
        else:
            logger.debug("Load targets: %s", comic_slugs)
            return comic_slugs

    def _try_load_comic_data(self, comic_slug: str) -> None:
        try:
            data = self._get_data(comic_slug)
            if self._should_load_data(data):
                self._load_data(data)
            else:
                logger.debug("Skipping inactive comic")
        except ComicDataError as error:
            logger.error(error)
        except Exception as error:
            logger.exception(error)

    def _get_data(self, comic_slug: str) -> ComicDataBase:
        logger.debug("Importing comic module for %s", comic_slug)
        comic_module = get_comic_module(comic_slug)
        if not hasattr(comic_module, "ComicData"):
            raise ComicDataError(
                "%s does not have a ComicData class" % comic_module.__name__
            )
        data = comic_module.ComicData()  # type: ignore
        assert isinstance(data, ComicDataBase)
        return data

    def _should_load_data(self, data: ComicDataBase) -> bool:
        if (
            data.active
            or self.include_inactive
            or Comic.objects.filter(slug=data.slug).exists()
        ):
            return True
        else:
            return False

    def _load_data(self, data: ComicDataBase) -> None:
        logger.debug("Updating database with: %s", data)
        Comic.objects.update_or_create(
            language=data.language,
            slug=data.slug,
            defaults={
                "name": data.name,
                "url": data.url,
                "active": data.active,
                "start_date": data.start_date,
                "end_date": data.end_date,
                "rights": data.rights,
            },
        )
