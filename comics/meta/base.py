import datetime

from comics.core.models import Comic

class MetaBase(object):
    # Required values
    name = None
    language = None
    url = None

    # Default values
    active = True
    start_date = None
    end_date = None
    rights = ''

    @property
    def slug(self):
        return self.__module__.split('.')[-1]

    def is_previously_loaded(self):
        return bool(Comic.objects.filter(slug=self.slug).count())

    def create_comic(self):
        if self.is_previously_loaded():
            comic = Comic.objects.get(slug=self.slug)
            comic.name = self.name
            comic.language = self.language
            comic.url = self.url
        else:
            comic = Comic(
                name=self.name,
                slug=self.slug,
                language=self.language,
                url=self.url)
        comic.active = self.active
        comic.start_date = self._get_date(self.start_date)
        comic.end_date = self._get_date(self.end_date)
        comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        if date is None:
            return None
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
