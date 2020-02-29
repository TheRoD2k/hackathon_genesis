from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.mainpage,name="mainpage"),
    path('signup/',views.signup,name='signup'),
    path('signin/',LoginView.as_view(),name='signin')

]