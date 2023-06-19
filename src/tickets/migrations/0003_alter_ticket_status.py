# Generated by Django 4.2.2 on 2023-06-18 19:26

from django.db import migrations, models

import tickets.constans


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="status",
            field=models.PositiveSmallIntegerField(
                default=tickets.constans.TicketStatus["NOT_STARTED"]
            ),
        ),
    ]
