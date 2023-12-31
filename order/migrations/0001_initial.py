# Generated by Django 3.2.20 on 2023-07-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LikedList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Like", "Like"), ("Dislike", "Dislike")],
                        default="Like",
                        max_length=10,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(editable=False, max_length=5)),
                ("first_name", models.CharField(max_length=10)),
                ("last_name", models.CharField(max_length=10)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("address", models.CharField(blank=True, max_length=150)),
                ("city", models.CharField(blank=True, max_length=20)),
                ("total", models.FloatField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Accepted", "Accepted"),
                            ("Preaparing", "Preaparing"),
                            ("OnShipping", "OnShipping"),
                            ("Completed", "Completed"),
                            ("Canceled", "Canceled"),
                        ],
                        default="New",
                        max_length=10,
                    ),
                ),
                ("ip", models.CharField(blank=True, max_length=20)),
                ("adminnote", models.CharField(blank=True, max_length=100)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("visual", models.CharField(blank=True, max_length=300, null=True)),
                ("price", models.FloatField()),
                ("amount", models.FloatField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Accepted", "Accepted"),
                            ("Canceled", "Canceled"),
                        ],
                        default="New",
                        max_length=10,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ShopCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("visual", models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
