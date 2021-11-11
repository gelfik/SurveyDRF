from django.urls import path, include

app_name = 'apiApp'

urlpatterns = [
    path('/users', include('UserProfileApp.urls', namespace='UserProfileApp')),
    path('/survey', include('SurveyApp.urls', namespace='SurveyApp')),
]