from rest_framework import serializers

from .models import PortfolioPhoto, Salon, Service

MAX_PHOTO_MB = 5


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "salon", "name", "category", "price_kes", "duration_minutes", "is_active")

    def validate_salon(self, salon):
        request = self.context["request"]
        if salon.owner_id != request.user.id:
            raise serializers.ValidationError("You can only add services to your own salon.")
        return salon


class PortfolioPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioPhoto
        fields = ("id", "salon", "service", "image", "caption", "created_at")
        read_only_fields = ("created_at",)

    def validate_image(self, image):
        if image.size > MAX_PHOTO_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Image must be under {MAX_PHOTO_MB}MB.")
        return image

    def validate(self, attrs):
        request = self.context["request"]
        salon = attrs.get("salon") or getattr(self.instance, "salon", None)
        if salon and salon.owner_id != request.user.id:
            raise serializers.ValidationError("You can only add photos to your own salon.")
        service = attrs.get("service")
        if service and salon and service.salon_id != salon.id:
            raise serializers.ValidationError("That service belongs to a different salon.")
        return attrs


class SalonListSerializer(serializers.ModelSerializer):
    cover_photo = serializers.SerializerMethodField()
    starting_price_kes = serializers.SerializerMethodField()

    class Meta:
        model = Salon
        fields = ("id", "slug", "name", "area", "landmark", "cover_photo", "starting_price_kes")

    def get_cover_photo(self, obj):
        photo = obj.photos.first()
        if not photo:
            return None
        request = self.context.get("request")
        url = photo.image.url
        return request.build_absolute_uri(url) if request else url

    def get_starting_price_kes(self, obj):
        prices = [s.price_kes for s in obj.services.all() if s.is_active]
        return min(prices) if prices else None


class SalonDetailSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    photos = PortfolioPhotoSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Salon
        fields = (
            "id", "slug", "name", "description", "area", "landmark",
            "latitude", "longitude", "phone", "is_active", "owner",
            "services", "photos", "created_at",
        )
        read_only_fields = ("slug", "created_at")
