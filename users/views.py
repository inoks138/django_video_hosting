from collections import namedtuple

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse

from .forms import UserRegisterForm, UserLoginForm, BuySubscriptionForm
from .models import User, UserSubscription


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрировались')

            if 'next' in request.GET:
                return redirect(request.GET['next'])

            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.GET:
                return redirect(request.GET['next'])

            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def profile(request, user_id=None):
    user = User.objects.get(pk=user_id) if user_id is not None else request.user

    context = {
        'user_profile': user,
    }

    return render(request, 'users/profile.html', context)


def subscription_list(request):
    Subscription = namedtuple('Subscription', 'term title price cost economy')

    subscriptions = (
        Subscription(
            term=1,
            title='1 месяц:',
            price=UserSubscription.get_price(1),
            cost=UserSubscription.get_cost(1),
            economy=False,
        ),
        Subscription(
            term=3,
            title='3 месяца:',
            price=UserSubscription.get_price(3),
            cost=UserSubscription.get_cost(3),
            economy=True,
        ),
        Subscription(
            term=6,
            title='6 месяцев:',
            price=UserSubscription.get_price(6),
            cost=UserSubscription.get_cost(6),
            economy=True,
        ),
        Subscription(
            term=12,
            title='12 месяцев:',
            price=UserSubscription.get_price(12),
            cost=UserSubscription.get_cost(12),
            economy=True,
        )
    )

    context = {
        'subscriptions': subscriptions,
        'price_for_one_month': UserSubscription.SUBSCRIPTION_COST,
    }

    return render(request, 'users/subscription_list.html', context)


def buy_subscription(request, months):
    if not request.user.is_authenticated:
        if 'next' in request.GET:
            return redirect('%s?next=%s?next=%s' % (reverse('login'), request.path, request.GET['next']))
        else:
            return redirect('%s?next=%s' % (reverse('login'), request.path))

    if request.method == 'POST':
        form = BuySubscriptionForm(request.POST)
        if form.is_valid():
            request.user.extend_subscription(months, UserSubscription.get_cost(months))

            if 'next' in request.POST:
                return redirect(request.POST['next'])

            return redirect('home')

    context = {
        'months': months,
        'cost': UserSubscription.get_cost(months),
        'form': BuySubscriptionForm,
    }

    return render(request, 'users/buy_subscription.html', context)
