# Generated by Django 4.1.6 on 2023-04-06 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0002_seller_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="seller",
            options={"ordering": ["name", "user__email"]},
        ),
        migrations.AlterModelOptions(
            name="usermodel",
            options={"ordering": ["lastName", "firstName"]},
        ),
    ]