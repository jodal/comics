from django.db import models

class ComicManager(models.Manager):
    def sort_by_name(self):
        qs = self.get_query_set()
        qs = qs.extra(select={'lower_name': 'LOWER(name)'})
        qs = qs.extra(order_by=['lower_name'])
        return qs
