# Generated by Django 3.2.20 on 2023-07-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_rating_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="settings",
            name="company",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
