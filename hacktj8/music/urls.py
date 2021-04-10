from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='/')
]
