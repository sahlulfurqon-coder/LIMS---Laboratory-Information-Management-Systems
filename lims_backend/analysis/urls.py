from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisResultViewSet, AnalysisParameterViewSet

router = DefaultRouter()
router.register(r'results', AnalysisResultViewSet, basename='analysisresult')
router.register(r'parameters', AnalysisParameterViewSet, basename='analysisparameter')

urlpatterns = [
    path('', include(router.urls)),
]
