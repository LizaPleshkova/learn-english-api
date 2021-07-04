import datetime
from django.db import models


class PollQuestion(models.Model):
    question_text = models.CharField(verbose_name="Вопрос опроса", max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = datetime.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def choices(self):
        if not hasattr(self, '_choices'):
            self._choices = self.choice.all()
        return self._choices

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class PollChoice(models.Model):
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(verbose_name="Вариант ответа", max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
