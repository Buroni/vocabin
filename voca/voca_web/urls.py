from django.urls import path

from . import views

app_name = 'voca_web'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('languages/', views.languages, name='languages'),
]
