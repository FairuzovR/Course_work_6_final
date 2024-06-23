from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from common.views import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации, виджеты для добавления аттрибутов
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма для профиля, виджеты для добавления аттрибутов
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    first_name = forms.CharField(
        required=False,
        max_length=30,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        required=False,
        max_length=30,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    phone = forms.CharField(
        required=False,
        max_length=15,
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш номер телефона'
        })
    )
    avatar = forms.ImageField(
        required=False,
        label='Аватар',
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        """
        * На этапе инициализации
        * Выдергиваем поле password из формы
        """
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)

    class Meta:
        model = User
        fields = (
            "email", "first_name", "last_name", "phone", "avatar", "country"
        )


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации, виджеты для добавления аттрибутов
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'name@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': 'Пароль'
        })
    )
