import logging
from typing import Any

from django.core.management.base import BaseCommand

VERBOSITY_LOG_LEVELS = {
    0: logging.ERROR,
    1: logging.INFO,
}


class ComicsBaseCommand(BaseCommand):
    """Base command that maps --verbosity to the root logger's level.

    Handlers and formats are configured by the LOGGING setting.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        logging.root.setLevel(
            VERBOSITY_LOG_LEVELS.get(options["verbosity"], logging.DEBUG)
        )
