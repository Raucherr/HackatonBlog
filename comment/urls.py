from django.urls import path

from comment.views import CommentListView

urlpatterns = [

    path('comments-list/', CommentListView.as_view())
]