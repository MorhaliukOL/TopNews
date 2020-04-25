from django.urls import path
from .views import (PostCreateView, PostUpdateView,
                    PostListView, PostDeleteView, post_detail)


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('detail/<slug:slug>', post_detail, name='post_detail'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('all/', PostListView.as_view(), name='post_list'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
]
