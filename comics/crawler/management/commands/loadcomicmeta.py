from comics.crawler.meta import ComicMetaLoader
from comics.utils.commands import ComicsBaseCommand, make_option

class Command(ComicsBaseCommand):
    option_list = ComicsBaseCommand.option_list + (
        make_option('-c', '--comic',
            action='append', dest='comic_slugs', metavar='COMIC',
            help='Comic to crawl, repeat for multiple [default: all]'),
    )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        comic_meta_loader = ComicMetaLoader(options)
        try:
            comic_meta_loader.start()
        except KeyboardInterrupt:
            comic_meta_loader.stop()
