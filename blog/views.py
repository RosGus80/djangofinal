from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView, DetailView

from blog.forms import PostCreateForm
from blog.models import Post


# Create your views here.


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'blog/post/create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:blog')

    def test_func(self):
        if self.request.user.groups.filter(name='content_manager').exists():
            return True
        else:
            return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post/create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:blog')

    def test_func(self):
        if self.request.user.groups.filter(name='content_manager').exists():
            return True
        else:
            return False


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = self.request.user.groups.filter(name='content_manager').exists()
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post/delete.html'
    success_url = reverse_lazy('blog:blog')

    def test_func(self):
        if self.request.user.groups.filter(name='content_manager').exists():
            return True
        else:
            return False


class PostListView(TemplateView):
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Post.objects.all()
        context['is_content_manager'] = self.request.user.groups.filter(name='content_manager').exists()
        return context

