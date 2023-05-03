# django and python imports

# rest framework imports
from crypt import methods
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# local imports
from surveys.models import *
from surveys.serializers import *
from surveys.utils import formatter

from utils import responses
from utils import permissions as custom_permissions


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in [
            "list",
            "create",
            "retrieve",
            "update",
            "partial_update",
            "delete",
            "destroy",
            "getSurveysForProject",
        ]:
            permission_classes = [custom_permissions.IsAdmin]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    """
        Get all Projects endpoint
    """

    def list(self, request, format=None):
        projects = Project.objects.all()

        return responses.SuccessResponseHandler(
            True,
            "Successfully found all the projects .",
            formatter.multipleProjectFormatter(projects),
        )

    """
        Get a Project By Id
    """

    def retrieve(self, request, format=None, pk=None):
        # checks the project
        checkProject = Project.objects.filter(pk=pk)
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project Not found.")

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the customer data",
            formatter.singleProjectFormatter(checkProject[0]),
        )

    """
        Create Project endpoint
    """

    def create(self, request, format=None):
        if (
            not "name"
            or not "description"
            or not "customer_id"
            or not "location"
            or not "noOfDataCollectors"
            or not "budget" in request.data.keys()
        ):
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks the project with the name already exists
        checkProject = Project.objects.filter(name=request.data["name"])
        if checkProject.exists():
            return responses.BadRequestErrorHandler("Project already exists")

        # checks the customer with the id
        checkCustomer = Customer.objects.filter(pk=request.data["customer_id"])
        if not checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer not found")

        # creates the project
        createdProject = Project.objects.create(
            name=request.data["name"],
            description=request.data["description"],
            customer=checkCustomer[0],
            location=request.data["location"],
            noOfDataCollectors=request.data["noOfDataCollectors"],
            budget=request.data["budget"],
        )

        return responses.SuccessResponseHandler(
            True,
            "Successfully Created the Project .",
            formatter.singleProjectFormatter(createdProject),
        )

    """
        Edit Project Endpoint
    """

    def update(self, request, format=None, pk=None):
        # checks the project with the name already exists
        checkProject = Project.objects.filter(pk=pk)
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project not Found")

        # checks all the required fields
        if (
            not "name"
            or not "description"
            or not "location"
            or not "noOfDataCollectors"
            or not "budget" in request.data.keys()
        ):
            return responses.BadRequestErrorHandler("All required fields must be input")

        checkProject.update(
            name=request.data["name"],
            description=request.data["description"],
            location=request.data["location"],
            noOfDataCollectors=request.data["noOfDataCollectors"],
            budget=request.data["budget"],
        )

        return responses.SuccessResponseHandler(
            True,
            "Successfully Created the Customer",
            formatter.singleProjectFormatter(checkProject[0]),
        )

    """
        Delete Project Endpoint
    """

    def destroy(self, request, format=None, pk=None):
        # checks the project with the name already exists
        checkProject = Project.objects.filter(pk=pk)
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project not Found")

        checkProject.delete()

        return responses.SuccessResponseHandler(True, "Project Deleted", None)

    """
        Get all surveys for project
    """

    @action(detail=True, methods=["GET"])
    def getSurveysForProject(self, request, format=None, pk=None):
        # checks the project with the id
        checkProject = Project.objects.filter(pk=pk)
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project Not Found.")

        projectSurveys = Survey.objects.filter(project=checkProject[0])

        if not projectSurveys.exists():
            # return Response(" No surveys exist for this project . Please create surveys for it . " ,status=status.HTTP_200_OK)
            return Response(
                {
                    "success": False,
                    "message": "No surveys exist for this project . Please create surveys for it .",
                }
            )

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the surveys for the customer",
            formatter.multipleSurveyFormatter(projectSurveys),
        )
