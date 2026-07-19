from __future__ import annotations

from typing import TYPE_CHECKING, Any

from comics.core.comic_data import ComicDataLoader, Options
from comics.core.command_utils import ComicsBaseCommand

if TYPE_CHECKING:
    from argparse import ArgumentParser


class Command(ComicsBaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-c",
            "--comic",
            action="append",
            dest="comic_slugs",
            metavar="COMIC",
            help=(
                'Comic to add to site, repeat for multiple. Use "-c all" to add all.'
            ),
        )

    def handle(self, *args: Any, **options: Any) -> None:
        super().handle(*args, **options)
        data_loader = ComicDataLoader(Options(comic_slugs=options["comic_slugs"] or []))
        try:
            data_loader.start()
        except KeyboardInterrupt:
            data_loader.stop()
