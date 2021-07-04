# Generated by Django 3.2.4 on 2021-06-28 14:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0014_auto_20210628_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 17, 36, 53, 651120), verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='score',
            field=models.FloatField(default=0.0, verbose_name='Кол-во баллов'),
        ),
    ]