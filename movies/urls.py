from django.urls import path

from movies.views import home, FilmCatalog, SeriesCatalog, AnimationCatalog, watch

urlpatterns = [
    path('', home, name="home"),
    path('films', FilmCatalog.as_view(), name="films"),
    path('series', SeriesCatalog.as_view(), name="series"),
    path('animation', AnimationCatalog.as_view(), name="animation"),
    path('watch/<url>', watch, name="watch")
]
