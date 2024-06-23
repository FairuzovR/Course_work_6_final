import smtplib
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from config import settings
from mailing.models import MailingSettings, MailingStatus


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.filter(
        setting_status__in=['Create', 'Started']
    )

    for mailing in mailings:
        if mailing.end_time < current_datetime:
            mailing.setting_status = 'Done'
            mailing.save()
            continue

        if mailing.last_sent_datetime > current_datetime:
            continue
        if mailing.last_sent_datetime <= current_datetime:
            title = mailing.message.title
            content = mailing.message.content

            try:
                server_response = send_mail(
                    subject=title,
                    message=content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email for recipient in mailing.recipients.all()],
                    fail_silently=False,
                )

                if server_response == 1:
                    mailing.setting_status = 'Started'
                    mailing.last_sent_datetime = current_datetime
                    MailingStatus.objects.create(
                        status='success',
                        mailing_response='Письмо успешно отправлено',
                        mailing_list=mailing
                    )

                    if mailing.sending == 'daily':
                        mailing.last_sent_datetime = current_datetime + timedelta(days=1)
                    elif mailing.sending == 'weekly':
                        mailing.last_sent_datetime = current_datetime + timedelta(weeks=1)
                    elif mailing.sending == 'monthly':
                        next_month = current_datetime + relativedelta(months=1)
                        mailing.last_sent_datetime = next_month.replace(day=1)
                    mailing.save()

            except smtplib.SMTPException as error:
                mailing.setting_status = 'Failed'
                mailing.save()
                MailingStatus.objects.create(
                    status='fail',
                    mailing_response=str(error),
                    mailing_list=mailing
                )
