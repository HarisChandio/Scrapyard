from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrawlerSet

router = DefaultRouter()
router.register(r'', CrawlerSet, basename='crawler')

urlpatterns = [
    path('', include(router.urls)),
]
