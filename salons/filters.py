import django_filters

from .models import Salon, Service


class SalonFilter(django_filters.FilterSet):
    area = django_filters.CharFilter(field_name="area", lookup_expr="icontains")
    category = django_filters.ChoiceFilter(
        field_name="services__category", choices=Service.Category.choices, distinct=True
    )
    max_price = django_filters.NumberFilter(
        field_name="services__price_kes", lookup_expr="lte", distinct=True
    )

    class Meta:
        model = Salon
        fields = ["area", "category", "max_price"]
