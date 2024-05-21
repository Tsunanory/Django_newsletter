from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
from django_apscheduler.jobstores import DjangoJobStore
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
import logging

logger = logging.getLogger(__name__)


def send_newsletter(newsletter_id):
    Newsletter = apps.get_model('newsletter', 'Newsletter')
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        logger.info(f"Sending newsletter {newsletter_id} to clients")
        for client in newsletter.clients.all():
            logger.info(f"Sending email to {client.email}")
            send_mail(
                newsletter.message.topic,
                newsletter.message.content,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
        newsletter.status = 'S'
        newsletter.save()
        logger.info(f"Newsletter {newsletter_id} sent successfully")
    except Newsletter.DoesNotExist:
        logger.error(f"Newsletter {newsletter_id} does not exist")
        pass
    except Exception as e:
        newsletter.status = 'F'
        newsletter.save()
        logger.error(f"Error sending newsletter {newsletter_id}: {e}")
        # print(f"Error sending newsletter {newsletter_id}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.start()
    return scheduler

scheduler = start_scheduler()
