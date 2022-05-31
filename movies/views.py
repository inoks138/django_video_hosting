import re
from collections import namedtuple

from django.db.models import F
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from movies.models import Movie, Film, Series, Genre, Country
from movies.services import open_file


def home(request):
    return render(request, 'movies/home.html')


class MovieCatalog(ListView):
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['countries'] = Country.objects.all()
        Year = namedtuple('Year', 'title slug')
        years = [Year(f'{str(i)} год', str(i)) for i in range(2022, 2014, -1)]
        years.append(Year('2010-2015', '2010-2015'))
        years.append(Year('2005-2010', '2005-2010'))
        years.append(Year('2000-2005', '2000-2005'))
        years.append(Year('1995-2000', '1995-2000'))
        years.append(Year('1990-1995', '1990-1995'))
        years.append(Year('1985-1990', '1985-1990'))
        years.append(Year('1980-1985', '1980-1985'))
        years.append(Year('до 1980 года', 'before-1980'))
        context['years'] = years
        context['rates'] = range(9, 5, -1)

        if 'genres' in self.request.GET:
            genres_list = self.request.GET['genres'].split(',')
            genres = Genre.objects.only('title').filter(slug__in=genres_list)
            context['selected_genres'] = ', '.join([genre.title for genre in genres])
            context['movies'] = context['movies'].filter(genres__in=genres).distinct()

        if 'countries' in self.request.GET:
            countries_list = self.request.GET['countries'].split(',')
            countries = Country.objects.only('title').filter(slug__in=countries_list)
            context['selected_countries'] = ', '.join([country.title for country in countries])
            context['movies'] = context['movies'].filter(country__in=countries)

        if 'year' in self.request.GET:
            year = self.request.GET['year']

            if re.match(r'^\d{4}$', year):
                context['selected_year'] = year
                context['movies'] = context['movies'].filter(release_date__year=int(year))
            elif re.match(r'^\d{4}-\d{4}$', year):
                context['selected_year'] = year
                year_start, year_end = (int(year) for year in year.split('-'))
                context['movies'] = context['movies'].filter(release_date__year__range=(year_start, year_end))
            elif re.match(r'^before-\d{4}$', year):
                context['selected_year'] = year
                context['movies'] = context['movies'].filter(release_date__year__lte=int(year))

        if 'rate' in self.request.GET:
            pass

        if 'subscription' in self.request.GET:
            if self.request.GET['subscription'] == 'false':
                context['movies'] = context['movies'].filter(require_subscription=False)
            elif self.request.GET['subscription'] == 'true':
                context['movies'] = context['movies'].filter(require_subscription=True)

        if 'sort' in self.request.GET:
            sort_method = self.request.GET['sort']
            if sort_method == 'date':
                context['movies'] = context['movies'].order_by(F('release_date').desc(nulls_last=True))
            elif sort_method == 'budget':
                context['movies'] = context['movies'].order_by(F('budget').desc(nulls_last=True))

        return context


class FilmCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(type=Movie.FILM, is_animation=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Фильмы'
        context['url'] = reverse('films')
        context['genres'] = Genre.objects.filter(type__in=(Genre.FILM, Genre.ALL))

        return context


class SeriesCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(type=Movie.SERIES, is_animation=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Сериалы'
        context['url'] = reverse('series')
        context['genres'] = Genre.objects.filter(type__in=(Genre.FILM, Genre.ALL))

        return context


class AnimationCatalog(MovieCatalog):
    def get_queryset(self):
        return Movie.objects.select_related('age_limit').filter(is_animation=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Мультфильмы'
        context['url'] = reverse('animation')
        context['genres'] = Genre.objects.filter(type__in=(Genre.ANIMATION, Genre.ALL))

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
