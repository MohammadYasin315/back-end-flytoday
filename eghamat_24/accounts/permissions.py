from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsOwner(BasePermission):
    message = "شما مالک این حساب نیستید."  

    def has_object_permission(self, request, view, obj):
        if obj != request.user:
            raise PermissionDenied(detail=self.message) 
        return True