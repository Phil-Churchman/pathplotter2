# Generated by Django 4.2.7 on 2024-01-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("path_app", "0006_alter_node_unique_together_node_temp_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="node",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="node",
            constraint=models.UniqueConstraint(
                fields=("node_code", "category", "version", "temp"),
                name="unique_node_code",
            ),
        ),
    ]
