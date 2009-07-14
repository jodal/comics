from comics.utils import disk_import
from comics.utils.commands import ComicsBaseCommand, make_option

class Command(ComicsBaseCommand):
    option_list = ComicsBaseCommand.option_list + (
        make_option('-c', '--comic',
            action='append', dest='comics', metavar='COMIC',
            help='Comic to import, repeat for multiple [default: all]'),
    )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        disk_import.do_disk_import(options)
