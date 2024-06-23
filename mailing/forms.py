from django import forms

from common.views import StyleFormMixin
from mailing.models import MailingMessage, MailingSettings
from recipient.models import Recipient


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для рассылки
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        recipients = Recipient.objects.filter(owner=user)
        self.fields['recipients'].queryset = recipients
        messages = MailingMessage.objects.filter(owner=user)
        self.fields['message'].queryset = messages

    class Meta:
        model = MailingSettings
        fields = ('sending', 'recipients', 'message', 'end_time',)
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для сообщения
    """
    class Meta:
        model = MailingMessage
        fields = ('title', 'content',)
