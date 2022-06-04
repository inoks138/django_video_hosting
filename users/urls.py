from django.urls import path, include

from .views import user_register, user_login, user_logout, profile, subscription_list, buy_subscription

urlpatterns = [
    path('register', user_register, name="register"),
    path('login', user_login, name="login"),
    path('logout/', user_logout, name='logout'),
    path('subscription_list', subscription_list, name='subscription_list'),
    path('buy_subscription/<int:months>', buy_subscription, name='buy_subscription'),

    path('profile', profile, name='profile'),
    path('profile/<user_id>', profile, name='profile'),
]
