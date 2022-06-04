from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "class": "control",
                                                                 "autocomplete": "current-password"}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="Введите email:", widget=forms.EmailInput(attrs={
        "class": "control",
        "placeholder": "example@gmail.com"
    }))
    username = forms.CharField(help_text="Введите имя пользователя:", widget=forms.TextInput(attrs={
        "class": "control"
    }))
    password1 = forms.CharField(help_text="Введите пароль:", widget=forms.PasswordInput(attrs={
        "type": "password",
        "class": "control",
        "autocomplete": "new-password"
    }))
    password2 = forms.CharField(help_text="Введите пароль ещё раз:", widget=forms.PasswordInput(attrs={
        "type": "password",
        "class": "control",
        "autocomplete": "new-password"
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',)


class BuySubscriptionForm(forms.Form):
    is_paid = forms.BooleanField()

    class Meta:
        fields = ('is_paid', )
