# Generated by Django 4.1.6 on 2023-05-03 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0021_seller_authenticated_by_admin"),
    ]

    operations = [
        migrations.RenameField(
            model_name="seller",
            old_name="authenticated_by_admin",
            new_name="authenticated",
        ),
    ]
