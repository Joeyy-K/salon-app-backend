from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Salon(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="salons"
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    # People search by estate/landmark in Kenya, so keep both plus an optional map pin
    area = models.CharField(max_length=100, db_index=True, help_text="e.g. Ruiru, Kileleshwa")
    landmark = models.CharField(max_length=150, blank=True, help_text="e.g. Opposite Thika Road Mall")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, help_text="Format: 2547XXXXXXXX")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}-{self.area}") or "salon"
            slug, n = base, 1
            while Salon.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.area})"


class Service(models.Model):
    class Category(models.TextChoices):
        BRAIDS = "braids", "Braids"
        TWISTS = "twists", "Twists"
        WEAVES = "weaves", "Weaves & weave-ons"
        WIGS = "wigs", "Wigs & installs"
        NATURAL = "natural", "Natural hair care"
        RELAXER = "relaxer", "Relaxers & treatments"
        CUTS = "cuts", "Cuts & styling"
        OTHER = "other", "Other"

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=120, help_text="e.g. Knotless braids (medium)")
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.OTHER)
    price_kes = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - KES {self.price_kes}"


def portfolio_upload_path(instance, filename):
    return f"portfolio/salon_{instance.salon_id}/{filename}"


class PortfolioPhoto(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="photos")
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="photos"
    )
    image = models.ImageField(upload_to=portfolio_upload_path)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Photo {self.pk} - {self.salon.name}"
