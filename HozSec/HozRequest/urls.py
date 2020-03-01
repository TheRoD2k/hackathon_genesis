from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView


urlpatterns = [
        path('', mainpage,name="mainpage"),
        path('place_problem/',place_problem,name='place'),
        #path('public_problems/',public_problems,name='public'),
        #path('problem/',views.problem_info,name='info'),
        #path('your_problems/',views.your_problems,name='your'),
        path('signin/',signin,name='signin'),
        #path('problem_gained/',views.problem_gained,name='gained'),
        #path('signup/',views.signup,name='signup'),
    ]
