from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportsViewSet
from .views import ExternalAnalysisReportViewSet

router = DefaultRouter()
router.register('reports', ReportsViewSet, basename='reports')
router.register(r'external-analysis-reports', ExternalAnalysisReportViewSet, basename='external-analysis-reports')

urlpatterns = [
    path('', include(router.urls)),
]
