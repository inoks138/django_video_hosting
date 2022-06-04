from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    username = models.CharField(verbose_name="Имя пользователя", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Дата последнего входа', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    def is_subscribed(self) -> bool:
        """Returns true if user has paid for subscription else false"""
        subscriptions = self.subscriptions.all()
        if not subscriptions:
            return False
        last_subscription = subscriptions.order_by('end_on').first()
        return last_subscription.end_on >= date.today()

    def extend_subscription(self, months_count, paid_cost) -> None:
        """Extends or provides subscription for certain months"""
        subscriptions = self.subscriptions.all()
        if not subscriptions:
            start_on = date.today()
        else:
            last_subscription = subscriptions.order_by('end_on').first()
            today = date.today()
            if today > last_subscription.end_on:
                start_on = today
            else:
                start_on = last_subscription.end_on + timedelta(days=1)

        UserSubscription.objects.create(user=self,
                                        start_on=start_on,
                                        end_on=start_on + relativedelta(months=+months_count),
                                        cost=paid_cost)

    def get_end_date_of_subscription(self):
        subscriptions = self.subscriptions.all()
        if not subscriptions:
            return None
        else:
            last_subscription = subscriptions.order_by('end_on').first()
            return last_subscription.end_on

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserSubscription(models.Model):
    SUBSCRIPTION_COST = 4.99
    DEPRECIATION_FOR_THREE_MONTHS = 0.9
    DEPRECIATION_FOR_SIX_MONTHS = 0.75
    DEPRECIATION_FOR_TWELVE_MONTHS = 0.6

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="Пользователь")
    start_on = models.DateField(verbose_name="Начало")
    end_on = models.DateField(verbose_name="Конец")
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Создано")

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Оплата подписки {self.user.username}"

    @classmethod
    def get_price(cls, months_count) -> float:
        """Returns subscription cost for certain count of months"""
        if months_count <= 0:
            raise ValueError('Количество месяцев не может быть меньше единицы')

        if months_count < 3:
            return round(cls.SUBSCRIPTION_COST, 2)
        elif months_count < 6:
            return round(cls.SUBSCRIPTION_COST * cls.DEPRECIATION_FOR_THREE_MONTHS, 2)
        elif months_count < 12:
            return round(cls.SUBSCRIPTION_COST * cls.DEPRECIATION_FOR_SIX_MONTHS, 2)
        else:
            return round(cls.SUBSCRIPTION_COST * cls.DEPRECIATION_FOR_TWELVE_MONTHS, 2)

    @classmethod
    def get_cost(cls, months_count) -> float:
        """Returns subscription cost for certain count of months"""
        if months_count <= 0:
            raise ValueError('Количество месяцев не может быть меньше единицы')

        if months_count < 3:
            return round(cls.SUBSCRIPTION_COST*months_count, 2)
        elif months_count < 6:
            return round(cls.SUBSCRIPTION_COST*cls.DEPRECIATION_FOR_THREE_MONTHS*months_count, 2)
        elif months_count < 12:
            return round(cls.SUBSCRIPTION_COST*cls.DEPRECIATION_FOR_SIX_MONTHS*months_count, 2)
        else:
            return round(cls.SUBSCRIPTION_COST*cls.DEPRECIATION_FOR_TWELVE_MONTHS*months_count, 2)
