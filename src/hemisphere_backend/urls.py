from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework import permissions

# rest framework imports
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from hemisphere_backend.root_api import api_root

# local imports
from users import urls as UserUrls
from surveys import urls as SurveyUrls
# api documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    # API schema for our accounts
    openapi.Info(
        title="HEMISPHERE API DOCUMENTATION ",
       
        default_version="v1",
        description="Hemisohere API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dannyhd88@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    # defines the default django admin url
    path('admin/', admin.site.urls , name='admin-site'),
    #root
    path('root/', api_root, name='root'),

    # defines the app urls created
    path(r'users/',include(UserUrls)),
    path(r'surveys/',include(SurveyUrls)),

    # defines the refresh token and common urls
    path('users/token/refresh/',TokenRefreshView.as_view() ,name='refresh-token'),

    # API documentation urls
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"),


    path("redoc/", schema_view.with_ui("redoc",
         cache_timeout=0), name="schema-redoc"),

    path('openapi.yml',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)