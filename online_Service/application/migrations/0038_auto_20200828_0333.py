# Generated by Django 3.1 on 2020-08-28 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0037_auto_20200828_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='pincode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ordered',
            name='time',
            field=models.TimeField(default='03:33:48'),
        ),
    ]
