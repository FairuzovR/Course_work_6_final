from django.db import models

from recipient.models import Recipient
from users.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

NULLABLE = {'null': True, 'blank': True}
FREQUENCY_CHOICES = [
    ('daily', 'раз в день'),
    ('weekly', 'раз в неделю'),
    ('monthly', 'раз в месяц'),
]
STATUS_OF_NEWSLETTER = [
    ("Create", 'Создана'),
    ("Started", 'Отправлено'),
    ("Done", 'Завершена'),
]
LOGS_STATUS_CHOICES = [('success', 'успешно'), ('fail', 'неуспешно'),]


class MailingMessage(models.Model):
    """
    Модель для сообщения
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ("can_view_message", "Can view message"),
            ("can_edit_message", "Can edit message"),
            ("can_delete_message", "Can delete message"),
        ]

    def __str__(self):
        return self.title


class MailingSettings(models.Model):
    """
    Модель для рассылки
    """
    first_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало рассылки'
    )
    last_sent_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Поле для отслеживания периода'
    )
    end_time = models.DateTimeField(verbose_name='Конец рассылки')
    sending = models.CharField(
        max_length=50,
        choices=FREQUENCY_CHOICES,
        verbose_name='Период рассылки'
    )
    message = models.ForeignKey(
        MailingMessage,
        on_delete=models.CASCADE,
        verbose_name='Сообщения'
    )
    setting_status = models.CharField(
        max_length=50,
        choices=STATUS_OF_NEWSLETTER,
        verbose_name='Статус рассылки',
        default='Create'
    )
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
        permissions = [
            ("can_view_malling", "Can view malling"),
            ("can_edit_malling", "Can edit malling"),
            ("can_delete_malling", "Can delete malling"),
        ]

    def clean(self):
        if self.end_time and self.end_time < now():
            raise ValidationError('Дата окончания не может быть в прошлом.')

    def __str__(self):
        return (
            f'{self.message} отправляется каждый {self.sending} \
            с {self.first_datetime}'
        )


class MailingStatus(models.Model):
    """
    Модель для статуса
    """
    last_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='last_datetime'
    )
    status = models.CharField(
        max_length=50,
        choices=LOGS_STATUS_CHOICES,
        default='',
        verbose_name='статус попытки'
    )
    mailing_response = models.TextField(verbose_name='mailing_response')
    mailing_list = models.ForeignKey(
        MailingSettings,
        on_delete=models.CASCADE,
        verbose_name='рассылка'
    )
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.CASCADE,
        verbose_name='клиент рассылки',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Статус отправки'
        verbose_name_plural = 'Статусы отправки'
        permissions = [
            ("can_view_status_malling", "Can view status malling"),
        ]

    def __str__(self):
        return (f'{self.status} отправлялось {self.last_datetime}, \
                ответ сервера: {self.mailing_response}')
