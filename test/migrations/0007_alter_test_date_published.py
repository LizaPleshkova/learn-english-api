# Generated by Django 3.2.4 on 2021-06-24 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0006_alter_test_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 18, 42, 7, 68265), verbose_name='Дата публикации'),
        ),
    ]
