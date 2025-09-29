from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisParameterViewSet, AnalysisResultViewSet

router = DefaultRouter()
router.register(r'parameters', AnalysisParameterViewSet)
router.register(r'results', AnalysisResultViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

