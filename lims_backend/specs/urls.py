from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecificationViewSet

router = DefaultRouter()
router.register(r'', SpecificationViewSet, basename='specification')

urlpatterns = [
    path('', include(router.urls)),
]
