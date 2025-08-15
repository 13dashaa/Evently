from rest_framework import permissions


class IsTicketOrganizerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.event.organizer.pk == request.user.pk or request.user.is_staff
