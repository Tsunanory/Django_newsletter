from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)
    country = models.CharField(max_length=40, verbose_name='страна')

    token = models.CharField(max_length=100, verbose_name='token', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'can_see_all_the_users',
                'can_see_all_the_users'
            ),
            (
                'can_block_users',
                'can_block_users'
            ),

        ]

    def __str__(self):
        return self.email