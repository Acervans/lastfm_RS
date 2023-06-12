from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lastfm_preview', views.lastfm_preview, name='lastfm_preview'),
    path('vad_analysis', views.vad_analysis, name='vad_analysis'),
    path('recommendations', views.recommendations, name='recommendations'),

    path('user_scraper', views.user_scraper, name='user_scraper'),
    path('user_scraper/tracks', views.scrape_tracks, name='scrape_tracks'),
    path('user_scraper/artists', views.scrape_artists, name='scrape_artists'),
    path('user_scraper/albums', views.scrape_albums, name='scrape_albums'),
    path('user_scraper/tags', views.scrape_tags, name='scrape_tags'),
]