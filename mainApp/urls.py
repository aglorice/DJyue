from django.urls import path

from mainApp import views

urlpatterns = [
    path('index/',views.index),
    path('blog',views.blog)
]
