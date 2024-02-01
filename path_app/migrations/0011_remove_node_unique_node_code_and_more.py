# Generated by Django 4.2.7 on 2024-01-27 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("path_app", "0010_node_unique_node_text"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="node",
            name="unique_node_code",
        ),
        migrations.RemoveConstraint(
            model_name="node",
            name="unique_node_text",
        ),
        migrations.AlterUniqueTogether(
            name="node",
            unique_together={("node_text", "category", "version", "temp")},
        ),
    ]