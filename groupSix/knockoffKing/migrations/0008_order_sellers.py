# Generated by Django 4.1.6 on 2023-04-16 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0007_remove_orderhistory_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="sellers",
            field=models.ManyToManyField(to="knockoffKing.seller"),
        ),
    ]
