from django.urls import path

from .views import SurveyManageDetailView, SurveyListAPIView, SurveyCreateView, AskCreateView, AskManageDetailView, \
    SurveyGetAPIView, ResultGetAPIView, ResultCreateView

app_name = 'SurveyApp'

SurveyCreateView.http_method_names = ('post', 'options',)
SurveyManageDetailView.http_method_names = ('get', 'put', 'delete', 'options',)

AskCreateView.http_method_names = ('post', 'options',)
AskManageDetailView.http_method_names = ('get', 'put', 'delete', 'options',)

SurveyListAPIView.http_method_names = ('get', 'options',)
SurveyGetAPIView.http_method_names = ('get', 'options',)

ResultCreateView.http_method_names = ('post', 'options',)
ResultGetAPIView.http_method_names = ('get', 'options',)

urlpatterns = [
    path('/create', SurveyCreateView.as_view()),
    path('/manage/<int:pk>', SurveyManageDetailView.as_view()),

    path('/<int:surveyID>/create', AskCreateView.as_view()),
    path('/<int:surveyID>/manage/<int:pk>', AskManageDetailView.as_view()),

    path('/list', SurveyListAPIView.as_view()),
    path('/<int:pk>', SurveyGetAPIView.as_view()),

    path('/result/answer', ResultCreateView.as_view()),
    path('/result/<int:user_id>', ResultGetAPIView.as_view()),

]
