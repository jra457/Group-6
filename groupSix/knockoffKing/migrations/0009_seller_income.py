# Generated by Django 4.1.6 on 2023-04-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0008_order_sellers"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="income",
            field=models.BigIntegerField(default=0),
        ),
    ]
