import logging
import pytz
from django.db import models
from django_apscheduler.models import DjangoJob

from users.models import User
from .scheduler import send_newsletter, scheduler

logger = logging.getLogger(__name__)

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=50, **NULLABLE, verbose_name='имя')
    comment = models.TextField(verbose_name='комментарий')
    user = models.ForeignKey(User, verbose_name='создатель', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return self.email


class Message(models.Model):
    topic = models.CharField(max_length=50, verbose_name='заголовок')
    content = models.TextField(verbose_name='текст')
    user = models.ForeignKey(User, verbose_name='создатель', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.topic


class Newsletter(models.Model):
    STATUS = [
        ('S', 'Successful'),
        ('P', 'In Process'),
        ('F', 'Failed'),
    ]
    FREQ_OPTIONS = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ]
    initial = models.DateTimeField(verbose_name='начало рассылки')
    frequency = models.CharField(max_length=2, choices=FREQ_OPTIONS, default='W', verbose_name='частота рассылки')
    status = models.CharField(max_length=2, choices=STATUS, default='P', verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    user = models.ForeignKey(User, verbose_name='создатель', blank=True, null=True, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'P':
            job_id = f'send-newsletter-{self.id}'
            logger.info(f"Scheduling job {job_id} for {self.initial}")

            try:
                existing_job = DjangoJob.objects.get(id=job_id)
                scheduler.remove_job(job_id)
                existing_job.delete()
                logger.info(f"Removed existing job {job_id}")
            except DjangoJob.DoesNotExist:
                pass

            scheduler.add_job(
                send_newsletter,
                trigger='date',
                run_date=self.initial.astimezone(pytz.UTC),
                args=[self.id],
                id=job_id,
                replace_existing=True
            )
            logger.info(f"Scheduled new job {job_id} to run at {self.initial.astimezone(pytz.UTC)}")

    class Meta:
        verbose_name = 'рассылка'              
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                'can_view_any_newsletter',
                'can_view_any_newsletter'
            ),
            (
                'can_turn_the_newsletter_off',
                'can_turn_the_newsletter_off'
            )
        ]

    def __str__(self):
        return str(self.initial)


class Attempt(models.Model):
    STATUS = [
        ('S', 'Successful'),
        ('P', 'In Process'),
        ('F', 'Failed'),
    ]
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    last_attempt_time = models.DateTimeField()
    last_attempt_status = models.CharField(max_length=2, choices=STATUS, default='S')
    server_response = models.IntegerField(default=200)

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'

    def __str__(self):
        return f"{self.newsletter} to {self.client} at {self.last_attempt_time} - {self.last_attempt_status}"
