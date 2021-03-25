from django.conf import settings
from django.db import migrations, models

import comics.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "comic",
                    models.ForeignKey(to="core.Comic", on_delete=models.CASCADE),
                ),
            ],
            options={
                "db_table": "comics_user_profile_comics",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "secret_key",
                    models.CharField(
                        default=comics.accounts.models.make_secret_key,
                        help_text="Secret key for feed and API access",
                        max_length=32,
                    ),
                ),
                (
                    "comics",
                    models.ManyToManyField(
                        to="core.Comic", through="accounts.Subscription"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        related_name="comics_profile",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "comics_user_profile",
                "verbose_name": "comics profile",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="subscription",
            name="userprofile",
            field=models.ForeignKey(
                to="accounts.UserProfile", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
    ]
