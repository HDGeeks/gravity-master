# django and python imports

# rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# local imports
from surveys.models import *
from surveys.serializers import *
from surveys.utils import formatter
from users.serializers import UserSerializer

from utils import responses, token
from utils import permissions as custom_permissions


class DataCollectorViewset(viewsets.ModelViewSet):
    queryset = ExtendedUser.objects.filter(role__role="Data-Collector")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list", "getDataCollectors", "getAdmins"]:
            permission_classes = [custom_permissions.IsDataCollector]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def list(self, requets, format=None):
        # gets the user token from the request headers
        userToken = requets.headers["Authorization"]

        # gets the user
        user = token.getUserFromToken(userToken)

        # checks the surveys data collector is assigned to
        checkSurveys = Survey.objects.filter(dataCollectors__in=[user[1]]).distinct()

        return responses.SuccessResponseHandler(
            True,
            "Found surveys data collector is assigned to",
            formatter.multipleSurveyFormatter(checkSurveys),
        )
