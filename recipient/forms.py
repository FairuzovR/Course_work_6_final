from django import forms

from common.views import StyleFormMixin
from recipient.models import Recipient


class RecipientForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для тех, кому рассылаем сообщения
    """
    class Meta:
        model = Recipient
        fields = ('email', 'name', 'description',)
