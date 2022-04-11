from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from advertisement.views import *

router = DefaultRouter()
# router.register('ads', AdvertisementViewSet)
# router.register('categories', CategoriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
