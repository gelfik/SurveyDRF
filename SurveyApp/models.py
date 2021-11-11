from django.db import models
from django.utils.timezone import now as django_datetime_now
# Create your models here.
from UserProfileApp.models import User


class AskAnswerSelectionOnListAnswerModel(models.Model):
    answer = models.CharField('Ответ', default=None, max_length=255)
    validStatus = models.BooleanField('Верно/не верно', default=True)

    class Meta:
        verbose_name = 'Список ответов с выбором из списка овтетов'
        verbose_name_plural = 'Список ответов с выбором из списка овтетов'
        db_table = 'AskAnswerSelectionOnListAnswerModel'

    def __str__(self):
        return f'{self.answer}'


class AskModel(models.Model):
    ask = models.CharField('Вопрос', default=None, max_length=255)

    isMulti = models.BooleanField('Множественный выбор', default=False, null=True, blank=True)
    answerList = models.ManyToManyField(AskAnswerSelectionOnListAnswerModel, verbose_name='Ответы с выбором',
                                        blank=True)
    answerInput = models.CharField('Ответ с вводом текста', default=None, max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'AskModel'

    def __str__(self):
        return f'{self.ask}'


class SurveyModel(models.Model):
    name = models.CharField('Название', default='', max_length=255)
    description = models.TextField('Описание', default='')
    startDate = models.DateTimeField('Дата старта', default=django_datetime_now)
    endDate = models.DateTimeField('Дата окончания', default=django_datetime_now)
    askList = models.ManyToManyField(AskModel, verbose_name='Вопросы', blank=True)

    createUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель опроса', null=False)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        db_table = 'SurveyModel'

    def __str__(self):
        return f'{self.name}'


class ResultAnswerModel(models.Model):
    ask = models.ForeignKey(AskModel, on_delete=models.CASCADE, verbose_name='Вопрос', default=None)
    answerList = models.ManyToManyField(AskAnswerSelectionOnListAnswerModel, verbose_name='Ответы с выбором',
                                        default=None)
    answerInput = models.TextField('Ответ текстом', default=None, null=True, blank=True)
    answerValid = models.BooleanField('Статус решения', default=False)

    class Meta:
        verbose_name = 'Ответ пользоватля'
        verbose_name_plural = 'Ответы пользоватля'
        db_table = 'ResultAnswerModel'

    def __str__(self):
        return f'{self.ask}'


class ResultModel(models.Model):
    survey = models.ForeignKey(SurveyModel, on_delete=models.CASCADE, verbose_name='Опрос', default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', default=None, blank=True,
                             null=True)
    isAnon = models.BooleanField('Анонимное решение', default=False)
    resultList = models.ManyToManyField(ResultAnswerModel, verbose_name='Ответы', default=None)

    class Meta:
        verbose_name = 'Результат пользоватля'
        verbose_name_plural = 'Результаты пользоватля'
        db_table = 'ResultModel'

    def __str__(self):
        return f'{self.survey}'
