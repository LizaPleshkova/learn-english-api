# Generated by Django 3.2.4 on 2021-06-26 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0008_auto_20210626_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 15, 39, 32, 681344), verbose_name='Дата публикации'),
        ),
    ]
