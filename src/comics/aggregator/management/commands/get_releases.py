from __future__ import annotations

from typing import TYPE_CHECKING, Any

from comics.aggregator.command import Aggregator
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
            help="Comic to crawl, repeat for multiple [default: all]",
        )
        parser.add_argument(
            "-f",
            "--from-date",
            dest="from_date",
            metavar="DATE",
            default=None,
            help="First date to crawl [default: today]",
        )
        parser.add_argument(
            "-t",
            "--to-date",
            dest="to_date",
            metavar="DATE",
            default=None,
            help="Last date to crawl [default: today]",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        super().handle(*args, **options)
        aggregator = Aggregator(options=options)
        try:
            aggregator.start()
        except KeyboardInterrupt:
            aggregator.stop()
