# Generated by Django 3.1 on 2020-08-28 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0036_auto_20200823_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pincode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ordered',
            name='time',
            field=models.TimeField(default='02:55:33'),
        ),
    ]
