from django.db import models
NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=50, **NULLABLE, verbose_name='имя')
    comment = models.TextField(verbose_name='комментарий')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return self.email


class Message(models.Model):
    topic = models.CharField(max_length=50, verbose_name='заголовок')
    content = models.TextField(verbose_name='текст')

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

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return str(self.initial)


class Attempt(models.Model):
    STATUS = [
        ('S', 'Successful'),
        ('P', 'In Process'),
        ('F', 'Failed'),
    ]
    last_attempt_time = models.DateTimeField()
    last_attempt_status = models.CharField(max_length=2, choices=STATUS, default='S')
    server_response = models.IntegerField(default=200)
