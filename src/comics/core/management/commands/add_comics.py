from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.management.base import CommandError

from comics.core.command_utils import ComicsBaseCommand
from comics.core.metadata import load_metadata, select_comic_slugs

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

        requested: list[str] = options["comic_slugs"] or []
        if len(requested) == 0:
            msg = 'No comic given. Use "-c all" or "-c <comic>" to select comics.'
            raise CommandError(msg)

        try:
            load_metadata(select_comic_slugs(requested))
        except KeyboardInterrupt:
            self.stderr.write("Interrupted")
