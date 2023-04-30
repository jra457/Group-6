# Generated by Django 4.1.6 on 2023-04-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0009_seller_income"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seller",
            name="income",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]