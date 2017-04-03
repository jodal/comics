import logging
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_LOG_FORMAT = '%(asctime)s [%(process)d] %(name)-12s %(levelname)-8s ' \
    + '%(message)s'
CONSOLE_LOG_FORMAT = '%(levelname)-8s %(message)s'


class ComicsBaseCommand(BaseCommand):
    if not [option for option in BaseCommand.option_list
            if option.dest == 'verbosity']:
        option_list = BaseCommand.option_list + (
            make_option(
                '-v', '--verbosity', action='store', dest='verbosity',
                default='1', type='choice', choices=['0', '1', '2'],
                help=(
                    'Verbosity level; 0=minimal output, 1=normal output, '
                    '2=all output')),
        )

    def handle(self, *args, **options):
        self._setup_logging(int(options.get('verbosity', 1)))

    def _setup_logging(self, verbosity_level):
        logging.root.setLevel(logging.NOTSET)
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
