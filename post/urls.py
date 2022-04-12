from django.urls import path, include
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('post-create/', PostCreateView.as_view()),
    path('posts-list/', PostListView.as_view()),
    path('post-update/<int:pk>/', PostUpdateView.as_view()),
    path('post-delete/<int:pk>/', PostDeleteView.as_view())
]
