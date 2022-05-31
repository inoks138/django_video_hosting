from django.db import models
from django.db.models import Avg
from django.urls import reverse

from config.settings import AUTH_USER_MODEL
from movies.validators import validate_video_file


class Genre(models.Model):
    FILM = 'film'
    ANIMATION = 'animation'
    ALL = 'all'
    GENRE_TYPES = (
        (FILM, 'film'),
        (ANIMATION, 'animation'),
        (ALL, 'all'),
    )
    title = models.CharField(max_length=50, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=GENRE_TYPES, default=ALL)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']

    def __str__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['title']

    def __str__(self):
        return self.title


class AgeLimit(models.Model):
    title = models.CharField(max_length=5, unique=True, verbose_name="Название")
    required_age = models.IntegerField(verbose_name="Требуемый возраст")

    class Meta:
        verbose_name = 'Возрастное ограничение'
        verbose_name_plural = 'Возрастные ограничения'
        ordering = ['required_age']

    def __str__(self):
        return f"{self.title} ({self.required_age}+)"


class Person(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    roles = models.ManyToManyField('PersonRole', verbose_name="Роли")

    class Meta:
        verbose_name = 'Личность'
        verbose_name_plural = 'Личности'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonRole(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class Movie(models.Model):
    FILM = "film"
    SERIES = "series"

    MOVIE_TYPES = (
        (FILM, "film"),
        (SERIES, "series"),
    )

    title = models.CharField(max_length=100, verbose_name="Название")
    url = models.SlugField(max_length=115, unique=True)
    description = models.TextField(verbose_name="Описание")
    type = models.CharField(choices=MOVIE_TYPES, max_length=6, default=FILM, verbose_name="Тип")
    genres = models.ManyToManyField('Genre', verbose_name="Жанры")
    age_limit = models.ForeignKey('AgeLimit', on_delete=models.SET_NULL, null=True,
                                  verbose_name="Возрастное ограничение")
    release_date = models.DateField(verbose_name="Дата выпуска")
    poster = models.ImageField(upload_to='movie_posters/%Y/%m/%d', verbose_name="Постер")
    is_animation = models.BooleanField(default=False, verbose_name='Мультфильм')

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Страна")
    writer = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='writer_movies', verbose_name="Сценарист")
    director = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='director_movies', verbose_name="Режиссер")
    budget = models.IntegerField(help_text="Указывать в долларах", null=True, blank=True, verbose_name="Бюджет")
    is_released = models.BooleanField(default=True, help_text="Вышло ли уже кино", verbose_name="Выпущено")

    require_subscription = models.BooleanField(default=False, verbose_name="Нужна подписка")
    require_purchase = models.BooleanField(default=False, verbose_name="Нужна покупка")
    price = models.IntegerField(null=True, blank=True, verbose_name="Цена")

    class Meta:
        verbose_name = 'Кино'
        verbose_name_plural = 'Кино'
        ordering = ['title']

    def save(self, **kwargs):
        super(Movie, self).save()
        if not self.url.endswith(str(self.pk)):
            self.url += '-' + str(self.id)
            super(Movie, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('watch', kwargs={'url': self.url})

    def count_rating(self):
        return self.rates.aggregate(Avg('rate'))


class MovieImages(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name="Кино")
    image = models.ImageField(upload_to='movie_images/%Y/%m/%d', verbose_name="Изображение")

    class Meta:
        verbose_name = 'Фотография из фильма'
        verbose_name_plural = 'Фотографии из фильма'

    def __str__(self):
        return f"Изображение {self.id} для кино {self.movie}"


class Trailers(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name="Кино")
    video = models.FileField(upload_to='movie_trailers/%Y/%m/%d', verbose_name="Видео",
                             validators=[validate_video_file])

    class Meta:
        verbose_name = 'Трейлер'
        verbose_name_plural = 'Трейлеры'

    def __str__(self):
        return f"Трейлер {self.id} для фильма {self.movie}"


class Film(Movie):
    video = models.FileField(upload_to='films/%Y/%m/%d', verbose_name="Видео", validators=[validate_video_file])

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f"{self.title}"


class Series(Movie):
    class Meta:
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'

    def __str__(self):
        return f"{self.title}"

    def get_episode(self, season_number=1, episode_number=1):
        return self.seasons.filter(number=season_number).first().episodes.filter(number=episode_number).first()


class Season(models.Model):
    series = models.ForeignKey('Series', on_delete=models.CASCADE, related_name='seasons', verbose_name="Сериал")
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="Название")
    number = models.IntegerField(verbose_name="Номер")

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'
        ordering = ['series', 'number']

    def __str__(self):
        return f"Сезон {self.number} - {self.title}" if self.title else f"Сезон {self.number}"

    def get_absolute_url(self):
        return reverse('watch', kwargs={
            'url': self.series.url,
            'season_number': self.number,
        })


class Episode(models.Model):
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='episodes', verbose_name="Сезон")
    video = models.FileField(upload_to='series/%Y/%m/%d', verbose_name="Видео", validators=[validate_video_file])
    title = models.CharField(max_length=75, null=True, blank=True, verbose_name="Название")
    number = models.IntegerField(verbose_name="Номер")

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        ordering = ['season', 'number']

    def __str__(self):
        return f"Серия {self.number} - {self.title}" if self.title else f"Серия {self.number}"

    def get_absolute_url(self):
        return reverse('watch', kwargs={
            'url': self.season.series.url,
            'season_number': self.season.number,
            'episode_number': self.number
        })


class MovieRate(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10

    MOVIE_RATES = (
        (ONE, 1),
        (TWO, 2),
        (THREE, 3),
        (FOUR, 4),
        (FIVE, 5),
        (SIX, 6),
        (SEVEN, 7),
        (EIGHT, 8),
        (NINE, 9),
        (TEN, 10),
    )

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='rates', verbose_name="Кино")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rates', verbose_name="Пользователь")
    rate = models.IntegerField(choices=MOVIE_RATES, verbose_name="Оценка")

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['movie']

    def __str__(self):
        return f"Оценка {self.user.username} - {self.rate}: {self.movie.title}"
