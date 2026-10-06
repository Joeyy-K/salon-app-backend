from rest_framework.routers import DefaultRouter

from .views import PortfolioPhotoViewSet, SalonViewSet, ServiceViewSet

router = DefaultRouter()
router.register("salons", SalonViewSet, basename="salon")
router.register("services", ServiceViewSet, basename="service")
router.register("photos", PortfolioPhotoViewSet, basename="photo")

urlpatterns = router.urls
