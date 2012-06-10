from comics.aggregator.command import Aggregator
from comics.core.command_utils import ComicsBaseCommand, make_option


class Command(ComicsBaseCommand):
    option_list = ComicsBaseCommand.option_list + (
        make_option('-c', '--comic',
            action='append', dest='comic_slugs', metavar='COMIC',
            help='Comic to crawl, repeat for multiple [default: all]'),
        make_option('-f', '--from-date',
            dest='from_date', metavar='DATE', default=None,
            help='First date to crawl [default: today]'),
        make_option('-t', '--to-date',
            dest='to_date', metavar='DATE', default=None,
            help='Last date to crawl [default: today]'),
    )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        aggregator = Aggregator(optparse_options=options)
        try:
            aggregator.start()
        except KeyboardInterrupt:
            aggregator.stop()
