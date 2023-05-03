# django and python imports
from django.db.models import Q

# rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# local imports
from users.models import *
from users.serializers import *
from users.utils import formatter
from utils import responses
from utils import permissions as custom_permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = ExtendedUser.objects.all()
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
            "addDataCollector",
            "getDataCollectors",
            "getAdmins",
        ]:
            permission_classes = [custom_permissions.IsAdmin]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    """
        User sign in method
    """

    @action(detail=False, methods=["POST"])
    def signin(self, request, format=None):
        if not "email" or not "password" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        # queries the user object by email
        user = ExtendedUser.objects.filter(email=request.data["email"])

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
        Add data collector
    """

    @action(detail=False, methods=["POST"])
    def addDataCollector(self, request, format=None):
        # check the required fields
        if (
            not "phone"
            or not "email"
            or not "first_name"
            or not "last_name"
            or not "username" in request.data.keys()
        ):
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
        checkDataCollectorRole = Role.objects.filter(role="Data-Collector")
        if not checkDataCollectorRole.exists():
            return responses.BadRequestErrorHandler(
                "Data Collector role does not exist."
            )

        # sets the password
        password = "9762" + request.data["username"] + "data"

        # creates the user
        createdUser = ExtendedUser.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            username=request.data["username"],
            phone=request.data["phone"],
            role=checkDataCollectorRole[0],
        )

        createdUser.set_password(password)
        createdUser.save()

        return responses.SuccessResponseHandler(
            True,
            "Created the data collector successfully",
            {
                "first_name": createdUser.first_name,
                "last_name": createdUser.last_name,
                "email": createdUser.email,
                "username": createdUser.username,
                "password": password,
                "phone": createdUser.phone,
            },
        )

    """
        Get List of data collectors
    """

    @action(detail=False, methods=["GET"])
    def getDataCollectors(self, request, format=None, pk=None):
        dataCollectors = ExtendedUser.objects.filter(role__role="Data-Collector")

        return responses.SuccessResponseHandler(
            True,
            "Successfully found data collectors",
            formatter.userFormatter(dataCollectors),
        )

    """
        Get List of Admins
    """

    @action(detail=False, methods=["GET"])
    def getAdmins(self, request, format=None, pk=None):
        admins = ExtendedUser.objects.filter(role__role="Admin")

        return responses.SuccessResponseHandler(
            True, "Successfully found admins", formatter.userFormatter(admins[1:])
        )
