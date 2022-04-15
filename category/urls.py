
from django.urls import path

from .views import CategoryListView

urlpatterns = [
    path('categories-list/', CategoryListView.as_view()),

]