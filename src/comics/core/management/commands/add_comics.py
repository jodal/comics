from __future__ import annotations

from typing import TYPE_CHECKING, Any

from comics.core.command_utils import ComicsBaseCommand
from comics.core.metadata import MetadataLoader, Options

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
        metadata_loader = MetadataLoader(
            Options(comic_slugs=options["comic_slugs"] or [])
        )
        try:
            metadata_loader.start()
        except KeyboardInterrupt:
            metadata_loader.stop()
