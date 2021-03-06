from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('logout/', views.logout,name="logout"),
    path('place_problem/',views.place_problem,name='place'),
    path('public_problems/',views.public_problems,name='public'),
    path('problem/<int:problem_id>/',views.problem_info,name='info'),
    path('userpage/',views.userpage,name='userpage'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('',views.place_problem,name='mainpage'),
    ]
