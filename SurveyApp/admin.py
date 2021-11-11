from django.contrib import admin

# Register your models here.
from SurveyApp.models import SurveyModel, AskModel, AskAnswerSelectionOnListAnswerModel, ResultModel, ResultAnswerModel

@admin.register(SurveyModel)
class SurveyModelAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'startDate', 'endDate', 'createUser',)


@admin.register(AskModel)
class AskModelAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'ask', 'isMulti',)


@admin.register(AskAnswerSelectionOnListAnswerModel)
class AskAnswerListAnswerModelAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'answer', 'validStatus',)


@admin.register(ResultModel)
class ResultModelAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'survey', 'user', 'isAnon',)


@admin.register(ResultAnswerModel)
class ResultAnswerModelAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'ask', 'answerValid',)
