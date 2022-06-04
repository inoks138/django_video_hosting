from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, UserSubscription


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login')
    list_display_links = ('username', 'email')


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'cost_wrap', 'start_on', 'end_on')
    list_display_links = ('id', )

    def username(self, obj):
        link = reverse("admin:users_user_change", args=[obj.user.id])
        return mark_safe(f'<a href="{link}">{obj.user.username}</a>')

    def cost_wrap(self, obj):
        return f"{obj.cost}$"

    username.short_description = 'Пользователь'
    cost_wrap.short_description = 'Стоимость'


admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
