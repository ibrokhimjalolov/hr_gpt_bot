# Generated by Django 4.1.1 on 2023-04-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gpt_bot", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="index",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="flowprocess",
            name="cv",
            field=models.URLField(blank=True, null=True),
        ),
    ]
