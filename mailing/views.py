from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import (MailingMessageForm,
                           MailingSettingsForm)
from mailing.models import MailingMessage, MailingSettings, MailingStatus
from mailing.services import get_blog_from_cache
from recipient.models import Recipient
from django.utils import timezone


class MailingMessageTemplateView(LoginRequiredMixin, TemplateView):
    """
    Представление для главной страницы
    """
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blogs'] = get_blog_from_cache()
        mailing_settings = MailingSettings.objects.all()
        context_data['mailing_settings'] = len(mailing_settings)
        active_mailings = MailingSettings.objects.filter(
            setting_status='Started'
        )
        context_data['active_mailings'] = len(active_mailings)
        recipients = Recipient.objects.all()
        context_data['recipient'] = len(recipients)
        return context_data


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания сообщения
    """
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления сообщения
    """
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.can_edit_message'

    def handle_no_permission(self):
        return redirect('mailing:list')


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления сообщений
    """
    model = MailingMessage
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.can_delete_message'

    def handle_no_permission(self):
        return redirect('mailing:list')


class MailingMessageListView(LoginRequiredMixin, ListView):
    """
    Представление для списка сообщений
    """
    model = MailingMessage
    permission_required = 'mailing.can_view_message'

    def handle_no_permission(self):
        return redirect('mailing:list')


class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра одного сообщения
    """
    model = MailingMessage


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания рассылок
    """
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def form_valid(self, form):
        settings = form.save()
        settings.owner = self.request.user
        settings.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления рассылок
    """
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')
    permission_required = 'mailing.can_edit_malling'

    def handle_no_permission(self):
        return redirect('mailing:settings_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsListView(LoginRequiredMixin, ListView):
    """
    Представление для списка рассылок
    """
    model = MailingSettings
    permission_required = 'mailing.can_view_malling'

    def handle_no_permission(self):
        return redirect('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра одной рассылки
    """
    model = MailingSettings
    permission_required = 'mailing.can_view_malling'

    def handle_no_permission(self):
        return redirect('mailing:settings_list')


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления рассылок
    """
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings_list')
    permission_required = 'mailing.can_delete_malling'

    def handle_no_permission(self):
        return redirect('mailing:settings_list')


class MailingStatusListView(LoginRequiredMixin, ListView):
    """
    Представление для списка статусов
    """
    model = MailingStatus
    permission_required = 'mailing.can_view_status_malling'

    def handle_no_permission(self):
        return redirect('mailing:settings_list')

    def get_queryset(self):
        return super().get_queryset().order_by('-last_datetime')[:20]
