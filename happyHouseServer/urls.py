from django.conf.urls import include
from django.urls import path

from happyHouseServer import views

urlpatterns = [
    # [POST] /api/signin 로그인
    path('signin/', views.UserSignInAPIView.as_view()),

    # [POST] /api/task 할 일 추가
    path('task/', views.AddHouseworkAPIView.as_view()),
]