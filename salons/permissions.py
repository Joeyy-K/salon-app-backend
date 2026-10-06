from rest_framework import permissions


class IsStylist(permissions.BasePermission):
    """Only users with the stylist role may create salons."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and getattr(request.user, "role", None) == "stylist"
        )


class IsSalonOwnerOrReadOnly(permissions.BasePermission):
    """Works for Salon objects and for objects that have a `salon` FK."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        salon = obj if hasattr(obj, "owner") else obj.salon
        return salon.owner_id == request.user.id
