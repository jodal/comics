import django.core.files.storage
from django.db import migrations, models

import comics.core.models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comic",
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
                    "name",
                    models.CharField(help_text="Name of the comic", max_length=100),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="For file paths and URLs",
                        unique=True,
                        max_length=100,
                        verbose_name="Short name",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        help_text="The language of the comic",
                        max_length=2,
                        choices=[("en", "English"), ("no", "Norwegian")],
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        help_text="URL to the official website",
                        verbose_name="URL",
                        blank=True,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True,
                        help_text="Wheter the comic is still being crawled",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        help_text="First published at", null=True, blank=True
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        help_text="Last published at, if comic has been cancelled",
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "rights",
                    models.CharField(
                        help_text="Author, copyright, and/or licensing information",
                        max_length=100,
                        blank=True,
                    ),
                ),
                (
                    "added",
                    models.DateTimeField(
                        help_text="Time the comic was added to the site",
                        auto_now_add=True,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "db_table": "comics_comic",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Image",
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
                    "file",
                    models.ImageField(
                        height_field="height",
                        storage=django.core.files.storage.FileSystemStorage(
                            base_url="/media/",
                            location="/home/jodal/dev/comics/run/media",
                        ),
                        width_field="width",
                        upload_to=comics.core.models.image_file_path,
                    ),
                ),
                ("checksum", models.CharField(max_length=64, db_index=True)),
                ("title", models.CharField(max_length=255, blank=True)),
                ("text", models.TextField(blank=True)),
                ("fetched", models.DateTimeField(auto_now_add=True)),
                ("height", models.IntegerField()),
                ("width", models.IntegerField()),
                (
                    "comic",
                    models.ForeignKey(to="core.Comic", on_delete=models.CASCADE),
                ),
            ],
            options={
                "db_table": "comics_image",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Release",
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
                    "pub_date",
                    models.DateField(verbose_name="publication date", db_index=True),
                ),
                (
                    "fetched",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "comic",
                    models.ForeignKey(to="core.Comic", on_delete=models.CASCADE),
                ),
                (
                    "images",
                    models.ManyToManyField(related_name="releases", to="core.Image"),
                ),
            ],
            options={
                "db_table": "comics_release",
                "get_latest_by": "pub_date",
            },
            bases=(models.Model,),
        ),
    ]
