from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from movies.models import Movie, Film, Series
from movies.services import open_file


def home(request):
    return render(request, 'movies/home.html')


class MovieCatalog(ListView):
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     return context


class FilmCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(type=Movie.FILM, is_animation=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Фильмы'
        context['url'] = reverse('films')

        return context


class SeriesCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(type=Movie.SERIES, is_animation=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Сериалы'
        context['url'] = reverse('series')

        return context


class AnimationCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(is_animation=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Мультфильмы'
        context['url'] = reverse('animation')

        return context


def watch(request, url, season_number=1, episode_number=1):
    item = Movie.objects.only('type').get(url=url)

    if item.type == Movie.FILM:
        movie = Film.objects.get(pk=item.pk)
        context = {
            'movie': movie,
        }
    else:
        movie = Series.objects.get(pk=item.pk)
        context = {
            'movie': movie,
            'seasons': movie.seasons.all(),
            'episodes': movie.seasons.filter(number=season_number).first().episodes.all(),
            'season_number': season_number,
            'episode_number': episode_number,
        }

    return render(request, 'movies/watch.html', context)


def get_streaming_video(request, url, season_number=1, episode_number=1):
    item = Movie.objects.only('type').get(url=url)

    if item.type == Movie.FILM:
        movie = Film.objects.get(pk=item.pk)
        video = movie.video
    else:
        movie = Series.objects.get(pk=item.pk)
        video = movie.get_episode(season_number=season_number, episode_number=episode_number).video

    file, status_code, content_length, content_range = open_file(request, video.path)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response
