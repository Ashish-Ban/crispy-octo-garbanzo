# Generated by Django 4.0 on 2021-12-16 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the product', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of product', max_digits=8)),
                ('code', models.CharField(help_text='Item code', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.DecimalField(decimal_places=2, help_text='Total Quantity or capacity for the product', max_digits=8)),
                ('available_quantity', models.DecimalField(decimal_places=2, help_text='Available Quantity for the selected product', max_digits=8)),
                ('product', models.OneToOneField(help_text='Product for which the stock is to be entered', on_delete=django.db.models.deletion.CASCADE, to='smartapp.product')),
            ],
        ),
    ]
