from django.db import models
from django.contrib.auth.models import User


class Hometask(models.Model):
    task = models.CharField(max_length=255, verbose_name='Задание')
    description = models.CharField(max_length=255, verbose_name='Описание ДЗ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hometask_user')

    def __str__(self):
        return f'{self.user.username} - {str(self.task)}'

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class CompletedHometask(models.Model):
    hometask = models.ForeignKey(Hometask, on_delete=models.CASCADE, related_name='hometask', default=0)
    file_txt = models.FileField(upload_to='homeTasks/', verbose_name='Файл с ДЗ', null=True)
    mark = models.IntegerField(verbose_name='Оценка', null=True)
    comment_admin = models.CharField(max_length=255, verbose_name='Комментарий по дз от админа', null=True)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField(verbose_name='Дата сдачи', null=True)

    def __str__(self):
        return f'{str(self.hometask)} - {str(self.mark)}'

    class Meta:
        verbose_name = 'Результат ДЗ'
        verbose_name_plural = 'Результаты ДЗ'
