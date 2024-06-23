from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    """
    Представление для списка блогов
    """
    model = Blog


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для одного блога
    """
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания блогов
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_add_blog'

    def form_valid(self, form):
        post = form.save()
        post.owner = self.request.user
        post.save()
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('blog:list')


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления блогов
    """
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_delete_blog'

    def handle_no_permission(self):
        return redirect('blog:list')


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление для обновления блогов
    """
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.can_edit_blog'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.get_object().id})

    def handle_no_permission(self):
        return redirect('blog:list')
