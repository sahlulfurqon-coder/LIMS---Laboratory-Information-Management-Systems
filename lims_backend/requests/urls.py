from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExternalRequestViewSet, ProductDevRequestViewSet
from .views import ExternalAnalysisResultViewSet

router = DefaultRouter()
router.register(r'external', ExternalRequestViewSet, basename='external-request')
router.register(r'product-dev', ProductDevRequestViewSet, basename='product-dev-request')
router.register(r'external-results', ExternalAnalysisResultViewSet, basename='external-results')


urlpatterns = [
    path('', include(router.urls)),
]
