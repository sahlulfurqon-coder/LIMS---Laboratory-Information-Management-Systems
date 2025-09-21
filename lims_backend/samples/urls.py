from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SampleTypeViewSet, RawMaterialViewSet, PackagingViewSet,
    FatBlendViewSet, FinishedProductViewSet, SampleViewSet
)

router = DefaultRouter()
router.register(r"sample-types", SampleTypeViewSet, basename="sampletype")
router.register(r"raw-materials", RawMaterialViewSet, basename="rawmaterial")
router.register(r"packaging", PackagingViewSet, basename="packaging")
router.register(r"fat-blends", FatBlendViewSet, basename="fatblend")
router.register(r"finished-products", FinishedProductViewSet, basename="finishedproduct")
router.register(r"samples", SampleViewSet, basename="sample")

urlpatterns = [
    path("", include(router.urls)),
]