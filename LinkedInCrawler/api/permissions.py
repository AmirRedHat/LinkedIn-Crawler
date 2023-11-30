from rest_framework.permissions import BasePermission


class AccessLevelPermissionOrAdmin(BasePermission):
   """ Allows vip users or admin users """
   
   def has_permission(self, request, view):
      cond1 = bool(request.user and request.user.is_authenticated and request.user.access_leve.lower() == "vip")
      cond2 = bool(request.user and request.user.is_staff)
      return cond1 or cond2