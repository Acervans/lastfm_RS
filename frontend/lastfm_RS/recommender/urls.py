from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lastfm_preview', views.lastfm_preview, name='lastfm_preview'),
]