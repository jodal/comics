from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.management.base import CommandError

from comics.aggregator.command import Aggregator, parse_date_range, select_comics
from comics.core.command_utils import ComicsBaseCommand
from comics.core.exceptions import ComicsError

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

        requested: list[str] = options["comic_slugs"] or []
        try:
            comics = select_comics(requested)
            from_date, to_date = parse_date_range(
                options["from_date"], options["to_date"]
            )
        except ComicsError as error:
            # ComicsError.__str__ wraps the message for logs, but the command
            # line wants just the message.
            raise CommandError(str(error.value)) from error

        try:
            Aggregator(comics, from_date=from_date, to_date=to_date).start()
        except KeyboardInterrupt:
            self.stderr.write("Interrupted")
