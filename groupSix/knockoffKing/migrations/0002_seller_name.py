# Generated by Django 4.1.6 on 2023-04-06 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="name",
            field=models.CharField(
                default="", help_text="Enter the store Name.", max_length=64
            ),
        ),
    ]