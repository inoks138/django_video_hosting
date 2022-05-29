from django.urls import path

from movies.views import home, FilmCatalog, SeriesCatalog, AnimationCatalog, watch, get_streaming_video

urlpatterns = [
    path('', home, name="home"),
    path('films', FilmCatalog.as_view(), name="films"),
    path('series', SeriesCatalog.as_view(), name="series"),
    path('animation', AnimationCatalog.as_view(), name="animation"),

    path('watch/<str:url>', watch, name="watch"),
    path('watch/<str:url>/<int:season_number>', watch, name="watch"),
    path('watch/<str:url>/<int:season_number>/<int:episode_number>/', watch, name="watch"),

    path('stream/<str:url>', get_streaming_video, name='stream'),
    path('stream/<str:url>/<int:season_number>', get_streaming_video, name='stream'),
    path('stream/<str:url>/<int:season_number>/<int:episode_number>', get_streaming_video, name='stream'),
]
