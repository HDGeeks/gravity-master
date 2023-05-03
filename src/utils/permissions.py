from math import perm
from rest_framework import permissions

from utils import token


class IsAdmin(permissions.BasePermission):
    """
    Permissions for Admins
    """

    message = "Restricted for Admins"

    def has_permission(self, request, view):
        """
        method that checks the admin by using the request header token
        """
        if token.checkAdminToken(request.headers) == True:
            return True
        else:
            return False


class IsDataCollector(permissions.BasePermission):
    """
    Permissions for Data Collectors
    """

    message = "Restricted for Data-Collectors"

    def has_permission(self, request, view):
        """
        method that checks the admin by using the request header token
        """
        if token.checkDataCollectorToken(request.headers) == True:
            return True
        else:
            return False
