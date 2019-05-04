from django.conf.urls import include
from django.urls import path

from happyHouseServer import views

urlpatterns = [
    # [POST] /api/signin 로그인
    path('signin/', views.UserSignInAPIView.as_view()),
]