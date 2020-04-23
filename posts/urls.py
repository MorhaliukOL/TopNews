from django.urls import path
from .views import (PostCreateView, PostDetailView, PostUpdateView,
                    PostListView, PostDeleteView)


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('all/', PostListView.as_view(), name='post_list'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
