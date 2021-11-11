from django.urls import path

from .views import (LoginAPIView)

app_name = 'UserProfileApp'

LoginAPIView.http_method_names = ('post', 'options',)

urlpatterns = [
    path('/login', LoginAPIView.as_view()),
]
