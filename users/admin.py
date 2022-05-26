from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login')
    list_display_links = ('username', 'email')


admin.site.register(User, UserAdmin)
