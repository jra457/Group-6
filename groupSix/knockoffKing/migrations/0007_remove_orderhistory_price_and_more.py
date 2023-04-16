# Generated by Django 4.1.6 on 2023-04-16 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("knockoffKing", "0006_orderhistory_delete_orderdetails"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderhistory",
            name="price",
        ),
        migrations.RemoveField(
            model_name="orderhistory",
            name="product",
        ),
        migrations.RemoveField(
            model_name="orderhistory",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="orderhistory",
            name="subTotal",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="dateAdded",
        ),
        migrations.AddField(
            model_name="order",
            name="subTotal",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.CreateModel(
            name="ActiveOrders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="knockoffKing.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="knockoffKing.usermodel",
                    ),
                ),
            ],
        ),
    ]
