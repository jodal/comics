# Generated by Django 3.2 on 2021-04-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_add_release_comic_pub_date_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comic",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
