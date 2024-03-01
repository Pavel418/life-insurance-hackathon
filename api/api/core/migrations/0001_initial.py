# Generated by Django 5.0.2 on 2024-03-01 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Driver",
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
                ("name", models.CharField(max_length=100)),
                ("vehicle_length", models.FloatField()),
                ("vehicle_weight", models.FloatField()),
                ("axles_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Trip",
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
                ("normal_entries", models.IntegerField()),
                ("vague_entries", models.IntegerField()),
                ("dangerous_entries", models.IntegerField()),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.driver"
                    ),
                ),
            ],
        ),
    ]
