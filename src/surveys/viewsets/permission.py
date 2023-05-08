from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import Role, ExtendedUser
from rest_framework.exceptions import AuthenticationFailed


class HasAdminRole(BasePermission):
    def has_permission(self, request, view):
        # Get the user from the JWT token in the Authorization header
        try:
            jwt_auth = JWTAuthentication()
            user, jwt_token = jwt_auth.authenticate(request)
        except AuthenticationFailed:
            return False

        # Check if the user has the "admin" role
        admin_role_id = Role.objects.filter(role="Admin").id
        if user.role == admin_role_id:
            return True

        return False


class HasDataCollectorRole(BasePermission):
    def has_permission(self, request, view):
        # Get the user from the JWT token in the Authorization header
        try:
            jwt_auth = JWTAuthentication()
            user, jwt_token = jwt_auth.authenticate(request)
        except AuthenticationFailed:
            return False

        # Check if the user has the "admin" role
        admin_role_id = Role.objects.filter(role="Data-Collector").id
        if user.role_id == admin_role_id:
            return True

        return False
