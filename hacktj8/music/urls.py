from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('genre', views.genre, name='genre'),
    path('generation', views.generation, name='generation'),
    path('splitter', views.splitter, name='splitter'),
    # path('upload_file', views.upload_file, name='upload_file')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)