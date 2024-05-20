import secrets
import string

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.http import HttpResponseRedirect
from django.urls import reverse

from config.settings import DEFAULT_FROM_EMAIL
from users.models import User

email = 'ivan.sklyaruk47@bk.ru'

class Command(BaseCommand):
    def handle(self, *args, **options):
        # email = input('email: ')
        # user_exists = User.objects.filter(email=email).exists()
        # if user_exists:
        #     user = User.objects.get(email=email)
        #     character = string.ascii_letters + string.digits
        #     password = "".join(secrets.choice(character) for i in range(12))
        #     user.set_password(password)
        #     user.save()
        #     print('password_setted')
        #     send_mail(
        #         subject="Восстановление пароля",
        #         message=f"Ваш пароль от сайта Shop изменен:\n"
        #                 f"Email: {email}\n"
        #                 f"Пароль: {password}",
        #         from_email=DEFAULT_FROM_EMAIL,
        #         recipient_list=[user.email]
        #     )
        #     print('mail sent')
        email = form.cleaned_data['email']

