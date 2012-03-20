from comics.meta.command import MetaLoader
from comics.utils.commands import ComicsBaseCommand, make_option

class Command(ComicsBaseCommand):
    option_list = ComicsBaseCommand.option_list + (
        make_option('-c', '--comic',
            action='append', dest='comic_slugs', metavar='COMIC',
            help='Comic to add to site, repeat for multiple [default: all]'),
    )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        meta_loader = MetaLoader(options)
        try:
            meta_loader.start()
        except KeyboardInterrupt:
            meta_loader.stop()
