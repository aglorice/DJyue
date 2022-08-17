from django.urls import path, include, re_path

from home import views

urlpatterns = [

    path('index/', views.index),  # 查看课表等等
    path('info_zfxt/', views.info_zfxt),
    re_path(r'check_code/', views.check_code),
    re_path(r'new_yzm/', views.new_yzm),
    path('loginout/', views.loginout),
    path('get_pinfo/', views.get_pinfo),
    path('get_message',views.get_message),
    path('get_grade/',views.get_grade)
]
