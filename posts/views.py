from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  ListView, DeleteView)

from .models import Post


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[Post.objects.last().pk])


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/detail_post.html'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'body']

    def get_success_url(self):
        return reverse('post_detail', args=[self.kwargs['pk']])


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/list_of_posts.html'
    ordering = ['-created']


class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/confirm_delete_post.html'
    success_url = reverse_lazy('post_list')

