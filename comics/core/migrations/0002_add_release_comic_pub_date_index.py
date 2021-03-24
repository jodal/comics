from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="release",
            index=models.Index(
                fields=["comic", "pub_date"],
                name="comics_rele_comic_i_2b6b41_idx",
            ),
        ),
    ]
