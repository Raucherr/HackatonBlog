from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]