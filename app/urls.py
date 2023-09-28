from django.urls import path
from . import views


urlpatterns = [
    path('', views.logins, name='login'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('upload', views.upload, name='upload'),
    path('result', views.prediction, name='result'),
    path('register', views.register, name='register'),

]
