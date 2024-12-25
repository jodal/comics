from django.db.models import TextChoices


class Language(TextChoices):
    EN = "en", "English"
    NO = "no", "Norwegian"
