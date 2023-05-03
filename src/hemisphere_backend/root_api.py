from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users-list": reverse("users-list", request=request, format=format),
            "users-add-data-collector": reverse(
                "users-addDataCollector", request=request, format=format
            ),
            "users-get-admins": reverse(
                "users-getAdmins", request=request, format=format
            ),
            "users-get-data-collectors": reverse(
                "users-getDataCollectors", request=request, format=format
            ),
            "users-sign-in": reverse("users-signin", request=request, format=format),
            # "users-detail":reverse('users-detail',request=request,format=format),
            "admin-list": reverse("admins-list", request=request, format=format),
            "admin-add-admin": reverse(
                "admins-addAdmin", request=request, format=format
            ),
            "admin-create-admin": reverse(
                "admins-createAdmin", request=request, format=format
            ),
            "admin-sign-in": reverse("admins-signin", request=request, format=format),
            "new-admin-sign-in": reverse(
                "new-admin-sign-in", request=request, format=format
            ),
            # "admin-detail":reverse('admins-detail',request=request,format=format),
            "data-collectors-list": reverse(
                "data-collectors-list", request=request, format=format
            ),
            # "data-collectors-detail":reverse('data-collectors-detail',request=request,format=format),
            "customers-list": reverse("customers-list", request=request, format=format),
            "projects-list": reverse("projects-list", request=request, format=format),
            "surveys-list": reverse("surveys-list", request=request, format=format),
            "language-list": reverse("language-list", request=request, format=format),
            "category-list": reverse("category-list", request=request, format=format),
            "questions-category-list": reverse(
                "questions-category-list", request=request, format=format
            ),
            "refresh-token": reverse("refresh-token", request=request, format=format),
            "admin-site": reverse("admin:login", request=request, format=format),
            # doc
            "swagger-api-doc": reverse(
                "schema-swagger-ui", request=request, format=format
            ),
            "redoc-api-doc": reverse("schema-redoc", request=request, format=format),
        }
    )
