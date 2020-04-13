from django.urls import path

from . import views

app_name = 'voca_web'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('languages/', views.languages, name='languages'),
    path('contact/', views.contact, name='contact'),
    path('tos/', views.tos, name='tos'),
    path('privacy/', views.privacy, name='privacy'),
]
