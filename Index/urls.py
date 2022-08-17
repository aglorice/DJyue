
from django.urls import path

from Index import views

urlpatterns = [
    path('login/',views.index),
    path('register/', views.register),
    path('surprise/', views.surprise),
    path('send_check_code/',views.send_check_code),
    path('is_user/',views.is_user),
    path('loginout/',views.logout),
    path('send_email/',views.send_email),
    path('re_email/',views.re_email),

]
