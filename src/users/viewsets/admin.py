# django and python imports
from django.db.models import Q

# rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status


# local imports
from users.models import *
from users.serializers import *
from utils import responses

from utils import permissions as custom_permissions


class AdminViewSet(viewsets.ModelViewSet):
    queryset = ExtendedUser.objects.filter(role__role="Admin")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in [
            "list",
            "create",
            "retrieve",
            "update",
            "partial_update",
            "delete",
            "destroy",
            "addAdmin",
        ]:
            permission_classes = [custom_permissions.IsAdmin]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    """
        An endpoint to create the first admin
    """

    @action(detail=False, methods=["POST"])
    def createAdmin(self, request, format=None):
        # checks all required attributes are input
        if (
            not "username"
            or not "email"
            or not "password"
            or not "first_name"
            or not "last_name"
            or not "middle_name"
            or not "phone" in request.data.keys()
        ):
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks the admin role
        checkAdminRole = Role.objects.filter(role="Admin")
        if not checkAdminRole.exists():
            return responses.BadRequestErrorHandler("Admin role does not exist")

        # checks if an admin already exists
        checkAdmin = ExtendedUser.objects.filter(role__role="Admin")
        username = request.data["email"]
        check_if_user_is_admin = (
            ExtendedUser.objects.filter(username=username).filter(role=1).distinct()
        )

        if check_if_user_is_admin.exists():
            return responses.BadRequestErrorHandler("Admin account already exists")

        # creates the admin account
        createdAdmin = ExtendedUser.objects.create(
            username=request.data["username"],
            email=request.data["email"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            middle_name=request.data["middle_name"],
            phone=request.data["phone"],
            role=checkAdminRole[0],
        )

        # sets the password for the newly created user
        createdAdmin.set_password(request.data["password"])
        createdAdmin.save()

        # gets the token for the newly created user to return in the response
        refresh = RefreshToken.for_user(createdAdmin)

        return responses.SuccessResponseHandler(
            True,
            "Successfully created the first admin",
            {"refresh": str(refresh), "access": str(refresh.access_token)},
        )

    """
        Admin sign in method
    """

    @action(detail=False, methods=["POST"])
    def signin(self, request, format=None):
        if not "email" or not "password" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        # check Admin role
        checkAdminRole = Role.objects.filter(role="Admin")
        if not checkAdminRole.exists():
            return responses.BadRequestErrorHandler("Admin role does not exist")

        # queries the user object by email
        user = ExtendedUser.objects.filter(
            email=request.data["email"], role=checkAdminRole[0]
        )

        if not user.exists():
            return responses.LoginErrorHandler()

        if not user[0].check_password(request.data["password"]):
            return responses.LoginErrorHandler()

        # gets the token for the found user to return in the response.
        refresh = RefreshToken.for_user(user[0])

        return responses.SuccessResponseHandler(
            True,
            "Succesfully logged in",
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user[0].email,
            },
        )

    """
        Create Admin Endpoint
    """

    @action(detail=False, methods=["POST"])
    def addAdmin(self, request, format=None):
        # check the required fields
        if not "phone" or not "email" or not "username" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks the user with the email or username already exists
        checkUser = ExtendedUser.objects.filter(
            Q(email=request.data["email"]) | Q(username=request.data["username"])
        )

        if checkUser.exists():
            return responses.BadRequestErrorHandler(
                "User with the email or username already exists."
            )

        # checks the data collector role
        checkAdminRole = Role.objects.filter(role="Admin")
        if not checkAdminRole.exists():
            return responses.BadRequestErrorHandler("Admin role does not exist.")

        # sets the password
        password = "0362" + request.data["username"] + "admin"

        # creates the admin
        createdUser = ExtendedUser.objects.create(
            email=request.data["email"],
            username=request.data["username"],
            phone=request.data["phone"],
            role=checkAdminRole[0],
        )

        createdUser.set_password(password)
        createdUser.save()

        return responses.SuccessResponseHandler(
            True,
            "Created the admin successfully",
            {
                "email": createdUser.email,
                "username": createdUser.username,
                "password": password,
                "phone": createdUser.phone,
            },
        )
