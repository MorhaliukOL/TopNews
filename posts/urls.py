from django.urls import path
from .views import (PostCreateView, PostUpdateView, UnapprovedPostListView,
                    PostListView, PostDeleteView, post_detail, approve_post, decline_post)


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('detail/<slug:slug>', post_detail, name='post_detail'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('all/', PostListView.as_view(), name='post_list'),
    path('unpublished/', UnapprovedPostListView.as_view(), name='posts_unpublished'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
    path('approve/<slug:slug>', approve_post, name='post_approve'),
    path('decline/<slug:slug>', decline_post, name='post_decline')
]
