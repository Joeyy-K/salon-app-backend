from django.contrib import admin

from .models import PortfolioPhoto, Salon, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "owner", "is_active", "created_at")
    list_filter = ("is_active", "area")
    search_fields = ("name", "area", "landmark")
    inlines = [ServiceInline]


admin.site.register(PortfolioPhoto)
