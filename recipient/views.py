from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from recipient.forms import RecipientForm
from recipient.models import Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    """
    Дженерик для списка людей в рассылке
    """
    model = Recipient


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """
    Дженерик для одного человека в рассылке
    """
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """
    Дженерик для создания человека в рассылке
    """
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipient:list')

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Дженерик для обновления человека в рассылке
    """
    model = Recipient
    form_class = RecipientForm
    # В таком виде ставятся права для обновления в данном случае
    permission_required = 'recipient.can_delete_blog'

    def handle_no_permission(self):
        """
        Обработчик; срабатывает, если нет нужных прав
        """
        return redirect('blog:list')

    def get_success_url(self):
        return reverse_lazy(
            'recipient:view',
            kwargs={'pk': self.get_object().id}
        )


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Дженерик для удаления человека в рассылке
    """
    model = Recipient
    success_url = reverse_lazy('recipient:list')
    permission_required = 'recipient.can_delete_blog'

    def handle_no_permission(self):
        return redirect('blog:list')
