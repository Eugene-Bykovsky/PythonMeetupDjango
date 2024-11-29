from rest_framework.permissions import BasePermission


class IsListenerOrSpeaker(BasePermission):
    """
    Permission для проверки, что пользователь является слушателем или докладчиком.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_listener() or request.user.is_speaker()
        )
