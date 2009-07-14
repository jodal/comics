import logging
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_LOG_FORMAT = '%(asctime)s [%(process)d] %(name)-12s %(levelname)-8s ' \
    + '%(message)s'
CONSOLE_LOG_FORMAT = '%(levelname)-8s %(message)s'

class ComicsBaseCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quiet',
            action='store_const', const=0, dest='verbose',
            help='Be quiet'),
        make_option('-v', '--verbose',
            action='store_const', const=2, dest='verbose',
            help='Be verbose'),
    )

    def handle(self, *args, **options):
        self._setup_logging(options.get('verbose', 1))

    def _setup_logging(self, verbosity_level):
        self._setup_file_logging()
        self._setup_console_logging(verbosity_level)

    def _setup_file_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format=FILE_LOG_FORMAT,
            datefmt=DATE_TIME_FORMAT,
            filename=settings.COMICS_LOG_FILENAME,
            filemode='a')

    def _setup_console_logging(self, verbosity_level):
        console = logging.StreamHandler()
        if verbosity_level == 0:
            console.setLevel(logging.ERROR)
        elif verbosity_level == 2:
            console.setLevel(logging.DEBUG)
        else:
            console.setLevel(logging.INFO)
        formatter = logging.Formatter(CONSOLE_LOG_FORMAT)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
