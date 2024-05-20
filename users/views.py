import random
import secrets
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm, RecoveryForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirmation/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserResetPasswordView(PasswordResetView):
    form_class = RecoveryForm
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            user = User.objects.get(email=email)
            character = string.ascii_letters + string.digits
            password = "".join(secrets.choice(character) for i in range(12))
            user.set_password(password)
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message=f"Ваш пароль от сайта Shop изменен:\n"
                        f"Email: {email}\n"
                        f"Пароль: {password}",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse('users:registration'))

