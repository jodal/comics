import datetime as dt

from comics.core.models import Comic

class MetaBase(object):
    # Required values
    name = None
    language = None
    url = None

    # Default values
    start_date = None
    end_date = None
    history_capable_date = None
    history_capable_days = None
    has_reruns = False
    schedule = ''
    rights = ''

    @property
    def slug(self):
        return self.__module__.split('.')[-1]

    def create_comic(self):
        if Comic.objects.filter(slug=self.slug).count():
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
        comic.start_date = self._get_date(self.start_date)
        comic.end_date = self._get_date(self.end_date)
        comic.history_capable_date = self._get_date(self.history_capable_date)
        comic.history_capable_days = self.history_capable_days
        comic.has_reruns = self.has_reruns
        comic.schedule = self.schedule
        comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        if date is None:
            return None
        return dt.datetime.strptime(date, '%Y-%m-%d').date()
