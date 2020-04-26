from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.utils.text import slugify
from django.views.generic import (CreateView, UpdateView,
                                  ListView, DeleteView)
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Post
from .forms import CommentForm


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        """Assign values to 'author' and 'slug' fields"""
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[Post.objects.last().slug])


def post_detail(request, slug):
    """Render Post detail view"""
    template_name = 'posts/detail_post.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment_form.instance.post = post
            comment_form.save()
        else:
            messages.error(request, 'Invalid data!')
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, template_name, context)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'body']

    def test_func(self):
        """
        Return True if current user is author of the post,
        or has 'approve posts' permission, and return False otherwise.
        """
        post_author = get_object_or_404(Post, slug=self.kwargs['slug']).author
        user = self.request.user
        return post_author == user or user.has_perm('posts.approve_post')

    def get_success_url(self):
        return reverse('post_detail', args=[self.kwargs['slug']])


class PostListView(ListView):
    approved = True
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/list_of_posts.html'
    ordering = ['-created']

    def get_queryset(self):
        """
        Return posts that are approved for publication,
        or aren't, depending on the value of 'approved' variable
        """
        return Post.objects.filter(approved=self.approved)


class UnapprovedPostListView(PostListView):
    approved = False


class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/confirm_delete_post.html'
    success_url = reverse_lazy('post_list')


def approve_post(request, slug):
    """Approve posts for publication"""
    post = get_object_or_404(Post, slug=slug)
    post.approved = True
    post.save()
    return redirect('post_detail', slug)


def decline_post(request, slug):
    """Decline posts from publication"""
    post = get_object_or_404(Post, slug=slug)
    post.approved = False
    post.save()
    return redirect('post_detail', slug)