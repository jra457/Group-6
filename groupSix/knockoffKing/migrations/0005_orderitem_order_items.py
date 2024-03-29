# Generated by Django 4.1.7 on 2023-04-13 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knockoffKing', '0004_seller_nameslug'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('dateAdded', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knockoffKing.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knockoffKing.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='knockoffKing.OrderItem', to='knockoffKing.product'),
        ),
    ]
