# Generated by Django 5.2 on 2025-05-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="description",
            field=models.TextField(default="No description provided"),
        ),
    ]
