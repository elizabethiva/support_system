# Generated by Django 4.2.2 on 2023-06-20 18:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="manager_tickets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="user_tickets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="request",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="messages",
                to="tickets.ticket",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
