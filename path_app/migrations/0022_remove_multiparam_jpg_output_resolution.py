# Generated by Django 4.2.7 on 2024-02-11 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("path_app", "0021_multiparam"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="multiparam",
            name="JPG_output_resolution",
        ),
    ]
