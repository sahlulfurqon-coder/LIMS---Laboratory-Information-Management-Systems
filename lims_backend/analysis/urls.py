from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisParameterViewSet, AnalysisResultViewSet

router = DefaultRouter()
router.register(r'parameters', AnalysisParameterViewSet, basename='parameters')
router.register(r'results', AnalysisResultViewSet, basename='results')

urlpatterns = [
    path("", include(router.urls)),
]


