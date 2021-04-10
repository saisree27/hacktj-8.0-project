from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('genre', views.genre, name='genre'),
    path('generation', views.generation, name='generation'),
]