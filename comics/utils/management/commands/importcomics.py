import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from comics.utils import disk_import

CONSOLE_LOG_FORMAT = '%(levelname)-8s %(message)s'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        # Not supported in disk_import
        #make_option('-q', '--quiet',
        #    action='store_const', const=0, dest='verbose',
        #    help='Be quiet'),
        #make_option('-v', '--verbose',
        #    action='store_const', const=2, dest='verbose',
        #    help='Be verbose'),
        make_option('-c', '--comic',
            action='append', dest='comics', metavar='COMIC',
            help='Comic to import, repeat for multiple [default: all]'),
    )

    def handle(self, *args, **options):
        self._setup_logging(options.get('verbose', 1))
        disk_import.do_disk_import(options)

    def _setup_logging(self, verbosity_level):
        if verbosity_level == 0:
            level = logging.WARNING
        elif verbosity_level == 2:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(
            format=CONSOLE_LOG_FORMAT,
            level=level,
        )
