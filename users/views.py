import random
import secrets
import string

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import ProfileForm, UserLoginForm, UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    """
    Дженерик для создания пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Вью-функция для подтверждения верификации
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    """
    Вью-функция для сброса пароля
    """
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                characters = string.ascii_letters + string.digits
                characters_list = list(characters)
                random.shuffle(characters_list)
                new_password = "".join(characters_list[:10])
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject="Восстановление пароля",
                    message=f"Здравствуйте, вы запрашивали обновление пароля. \
                        Ваш новый пароль: {new_password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                context['success_message'] = "Пароль успешно сброшен. \
                    Новый пароль был отправлен на ваш адрес электронной почты."
            else:
                context['error_message'] = "Пользователь с указанным адресом \
                    электронной почты не найден."
        else:
            context['error_message'] = "Необходимо указать адрес электронной \
                    почты для восстановления пароля."

    return render(request, "users/reset_password.html", context)


class ProfileView(UpdateView):
    """
    Дженерик для обновления пользователя
    """
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    """
    Дженерик для авторизации пользователя
    """
    template_name = "users/login.html"
    form_class = UserLoginForm
