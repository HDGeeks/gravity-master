from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "users-list":reverse('users-list',request=request,format=format),
        "admins-list":reverse('admins-list',request=request,format=format),
        "data-collectors-list":reverse('data-collectors-list',request=request,format=format),
        "customers-list":reverse('customers-list',request=request,format=format),
        "projects-list":reverse('projects-list',request=request,format=format),
        "surveys-list":reverse('surveys-list',request=request,format=format),
        "refresh-token":reverse('refresh-token',request=request,format=format),
        "admin-site":reverse('admin:login',request=request,format=format),

     
    })