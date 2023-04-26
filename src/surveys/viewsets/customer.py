# django and python imports

# rest framework imports
from urllib import response

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# local imports
from surveys.models import *
from surveys.serializers import *
from surveys.utils import formatter

from utils import responses 
from utils import permissions as custom_permissions

class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):

        if self.action in ['list','create','retrieve','update','partial_update','delete','destroy','getProjectsForCustomer']:
            permission_classes = [custom_permissions.IsAdmin]
        else:
            permission_classes = [AllowAny]
        
        return [permission() for permission in permission_classes]

    """
        Get all Customers endpoint
    """
    def list(self, request , format = None):

        customers = Customer.objects.all()

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the customer data",
            formatter.multipleCustomerFormatter(customers)
        )
        
    """
        Get a Customer By Id
    """
    def retrieve(self, request, format = None, pk = None):

        # checks the customer 
        checkCustomer = Customer.objects.filter(pk = pk)
        if not checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer Not found.")

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the customer data",
            formatter.singleCustomerFormatter(checkCustomer[0])
        )

    """
        Create Customer endpoint
    """
    def create(self, request , format = None):

        if not 'name' or not 'description' or not 'location' or not 'contact' in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks the customer with the name already exists
        checkCustomer = Customer.objects.filter(name = request.data['name'])
        if checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer with the name already exists.")

        # creates the customer
        createdCustomer = Customer.objects.create(
            name = request.data['name'],
            description = request.data['description'],
            location = request.data['location'],
            contact = request.data['contact']
        )

        return responses.SuccessResponseHandler(
            True,
            "Successfully Created the Customer",
            formatter.singleCustomerFormatter(createdCustomer)
        )

    """
        Edit Customer endpoint
    """
    def update(self, request , format = None, pk = None):
        # checks the customer with the name already exists
        
        checkCustomer = Customer.objects.filter(pk = pk)
        if not checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer does not exist")
        
        if not 'name' or not 'description' or not 'location' or not 'contact' in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")


        # edits the customer
        checkCustomer.update(
            name = request.data['name'],
            description = request.data['description'],
            location = request.data['location'],
            contact = request.data['contact']
        )

        return responses.SuccessResponseHandler(
            True,
            "Successfully Edited the Customer",
            formatter.singleCustomerFormatter(checkCustomer[0])
        )

    """
       Delete Customer Endpoint 
    """
    def destroy(self ,request , format = None, pk = None):
        # checks the customer with the name already exists
        
        checkCustomer = Customer.objects.filter(pk = pk)
        if not checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer does not exist")
        
        checkCustomer.delete()

        return responses.SuccessResponseHandler(
            True,
            "Successfully deleted the customer",
            {}
        )
    
    """
        Get all projects for customer 
    """
    @action(detail = True, methods =['GET'])
    def getProjectsForCustomer(self, request, format = None,pk = None):
        
        # checks the customer with the name already exists
        
        checkCustomer = Customer.objects.filter(pk = pk)
        if not checkCustomer.exists():
            return responses.BadRequestErrorHandler("Customer does not exist")
        
        customerProjects = Project.objects.filter(customer = checkCustomer[0])
        # if not customerProjects.exists():
        #     return responses.BadRequestErrorHandler("")
        
        return responses.SuccessResponseHandler(
            True,
            "Succesfully found projects for customer",
            formatter.multipleProjectFormatter(customerProjects)
        )