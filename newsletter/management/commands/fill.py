from django.core.management import BaseCommand, call_command
from newsletter.models import Newsletter, Message, Client, Attempt
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        Newsletter.objects.all().delete()
        Message.objects.all().delete()
        Client.objects.all().delete()
        User.objects.all().delete()
        Attempt.objects.all().delete()

        call_command('loaddata', 'fixtures/newsletter_app.json')
