from django.urls import path, include

from .views import user_register, user_login, user_logout, profile

urlpatterns = [
    path('register', user_register, name="register"),
    path('login', user_login, name="login"),
    path('logout/', user_logout, name='logout'),

    path('', profile, name='profile'),
    path('<user_id>', profile, name='profile'),
]
