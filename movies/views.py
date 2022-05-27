from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from movies.models import Movie, Film, Series


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


def watch(request, url):
    item = Movie.objects.only('type').get(url=url)

    if item.type == Movie.FILM:
        movie = Film.objects.get(pk=item.pk)
    else:
        movie = Series.objects.get(pk=item.pk)

    return render(request, 'movies/watch.html', {'movie': movie})

