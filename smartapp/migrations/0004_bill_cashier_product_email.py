# Generated by Django 4.0 on 2021-12-19 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('smartapp', '0003_alter_billitem_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='cashier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='email',
            field=models.EmailField(default='admin@smart.com', max_length=254),
        ),
    ]
