from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from movies.models import Genre, AgeLimit, Person, PersonRole, MovieImages, Trailers, Film, Series, Season, Episode, \
    MovieRate, Country


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ('title',)}


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ('title',)}


class AgeLimitAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'required_age')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_display_links = ('id', )
    search_fields = ('title', 'first_name', 'last_name')


class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id',)
    search_fields = ('title', )


class MovieImagesInline(admin.TabularInline):
    model = MovieImages
    extra = 0
    readonly_fields = ('thumbnail', )

    def thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100">')

    thumbnail.short_description = 'Миниатюра'


class TrailersImagesInline(admin.TabularInline):
    model = Trailers
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_genres', 'type', 'age_limit', 'release_date', 'thumbnail')
    list_display_links = ('id', 'title')
    list_filter = ('genres', 'age_limit')
    readonly_fields = ('thumbnail', )
    prepopulated_fields = {"url": ("title", )}
    inlines = [MovieImagesInline, TrailersImagesInline]

    def thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="75">')

    def get_genres(self, obj):
        return ', '.join(genre['title'] for genre in obj.genres.values('title').all())

    thumbnail.short_description = 'Постер'
    get_genres.short_description = 'Жанры'


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'series_ref')
    list_display_links = ('id', 'full_title')
    list_filter = ('series', )
    search_fields = ('series__title', )
    inlines = [EpisodeInline]

    def full_title(self, obj):
        return f"{obj.series}: {obj.number} сезон{f' - {obj.title}' if obj.title else ''}"

    def series_ref(self, obj):
        link = reverse("admin:movies_series_change", args=[obj.series.id])
        return mark_safe(f'<a href="{link}">{obj.series.title}</a>')

    full_title.short_description = 'Полное название'
    series_ref.short_description = 'Сериал'


class MovieRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_ref', 'username', 'rate')
    list_display_links = ('id', )
    search_fields = ('user__username', 'movie__title')

    def username(self, obj):
        link = reverse("admin:users_user_change", args=[obj.user.id])
        return mark_safe(f'<a href="{link}">{obj.user.username}</a>')

    def movie_ref(self, obj):
        link = reverse(f"admin:movies_{obj.movie.type}_change", args=[obj.movie.id])
        return mark_safe(f'<a href="{link}">{obj.movie.title}</a>')

    username.short_description = 'Пользователь'
    movie_ref.short_description = 'Кино'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(AgeLimit, AgeLimitAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonRole, PersonRoleAdmin)
admin.site.register(Film, MovieAdmin)
admin.site.register(Series, MovieAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(MovieRate, MovieRateAdmin)
