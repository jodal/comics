from comics.core.comic_data import ComicDataLoader
from comics.core.command_utils import ComicsBaseCommand


class Command(ComicsBaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-c', '--comic',
            action='append', dest='comic_slugs', metavar='COMIC',
            help=(
                'Comic to add to site, repeat for multiple. ' +
                'Use "-c all" to add all.'))

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        data_loader = ComicDataLoader(options)
        try:
            data_loader.start()
        except KeyboardInterrupt:
            data_loader.stop()
