from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .filters import SalonFilter
from .models import PortfolioPhoto, Salon, Service
from .permissions import IsSalonOwnerOrReadOnly, IsStylist
from .serializers import (
    PortfolioPhotoSerializer,
    SalonDetailSerializer,
    SalonListSerializer,
    ServiceSerializer,
)


class SalonViewSet(viewsets.ModelViewSet):
    """
    GET /api/salons/?area=ruiru&category=braids&max_price=3000&search=knotless
    """
    queryset = Salon.objects.filter(is_active=True).prefetch_related("services", "photos")
    permission_classes = [IsStylist, IsSalonOwnerOrReadOnly]
    filterset_class = SalonFilter
    search_fields = ["name", "area", "landmark", "services__name"]
    ordering_fields = ["created_at", "name"]
    lookup_field = "slug"

    def get_serializer_class(self):
        return SalonListSerializer if self.action == "list" else SalonDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True).select_related("salon")
    serializer_class = ServiceSerializer
    permission_classes = [IsSalonOwnerOrReadOnly]
    filterset_fields = ["salon", "category"]


class PortfolioPhotoViewSet(viewsets.ModelViewSet):
    queryset = PortfolioPhoto.objects.select_related("salon")
    serializer_class = PortfolioPhotoSerializer
    permission_classes = [IsSalonOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filterset_fields = ["salon", "service"]
