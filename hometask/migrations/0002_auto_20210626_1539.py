# Generated by Django 3.2.4 on 2021-06-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hometask', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedhometask',
            name='comment_admin',
            field=models.CharField(max_length=255, null=True, verbose_name='Комментарий по дз от админа'),
        ),
        migrations.AlterField(
            model_name='completedhometask',
            name='date_finished',
            field=models.DateTimeField(null=True, verbose_name='Дата сдачи'),
        ),
        migrations.AlterField(
            model_name='completedhometask',
            name='file_txt',
            field=models.FileField(null=True, upload_to='homeTasks/', verbose_name='Файл с ДЗ'),
        ),
        migrations.AlterField(
            model_name='completedhometask',
            name='mark',
            field=models.IntegerField(default=0, null=True, verbose_name='Оценка'),
        ),
    ]