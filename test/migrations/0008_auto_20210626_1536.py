# Generated by Django 3.2.4 on 2021-06-26 12:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0007_alter_test_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='test.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='test',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 15, 36, 18, 273014), verbose_name='Дата публикации'),
        ),
    ]