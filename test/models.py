from django.db import models
import datetime
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тест')
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    date_published = models.DateTimeField(verbose_name='Дата публикации', default=datetime.datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    '''
    '''
    title = models.CharField(max_length=255, verbose_name='Вопрос')
    test_id = models.ForeignKey(Test, related_name='questions', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Ответ')
    question_id = models.ForeignKey(Question, related_name='answers', on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField(verbose_name='Ответ правильный?', default=False)
    points = models.IntegerField(verbose_name='Кол-во баллов за ответ', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')
    score = models.FloatField(verbose_name='Кол-во баллов', default=0.0)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField(verbose_name='Дата прохождения', null=True)
    count_correct = models.IntegerField(default=0, verbose_name='Кол-во правильных ответов')
    count_incorrect = models.IntegerField(default=0, verbose_name='Кол-во неправильных ответов')

    def __str__(self):
        return f'{self.user.username} - {str(self.test.title)}'

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'


class AnswerUser(models.Model):
    test_result = models.ForeignKey(TestResult, related_name='answers_user', on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='answers', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{str(self.test_result.user.username)} - {str(self.question)} - {str(self.answer)}'

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
