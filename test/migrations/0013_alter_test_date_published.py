# Generated by Django 3.2.4 on 2021-06-27 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0012_alter_test_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 21, 30, 56, 770663), verbose_name='Дата публикации'),
        ),
    ]
