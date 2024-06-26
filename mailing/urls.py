from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingMessageCreateView, MailingMessageDeleteView,
                           MailingMessageDetailView, MailingMessageListView,
                           MailingMessageTemplateView,
                           MailingMessageUpdateView, MailingSettingsCreateView,
                           MailingSettingsDeleteView,
                           MailingSettingsDetailView, MailingSettingsListView,
                           MailingSettingsUpdateView, MailingStatusListView)

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingMessageTemplateView.as_view(), name='home'),
    path('list/', MailingMessageListView.as_view(), name='list'),
    path('create/', MailingMessageCreateView.as_view(), name='create'),
    path('view/<int:pk>/', MailingMessageDetailView.as_view(), name='view'),
    path('update/<int:pk>/', MailingMessageUpdateView.as_view(), name='edit'),
    path(
      'delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='delete'
    ),
    path(
      'settings_list/', MailingSettingsListView.as_view(), name='settings_list'
    ),
    path(
      'settings_create/',
      MailingSettingsCreateView.as_view(),
      name='settings_create'
    ),
    path(
      'settings_view/<int:pk>/',
      MailingSettingsDetailView.as_view(),
      name='settings_view'
    ),
    path(
      'settings_edit/<int:pk>/',
      MailingSettingsUpdateView.as_view(),
      name='settings_edit'
    ),
    path(
      'settings_delete/<int:pk>/',
      MailingSettingsDeleteView.as_view(),
      name='settings_delete'
    ),
    path(
      'status_mailing_list/',
      MailingStatusListView.as_view(),
      name='status_list'
    ),
]
