from django.urls import path
from app.views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('user', UserAPIView.as_view()),
    path('post', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostAPIView.as_view()),
]
