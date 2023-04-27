from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

# rest framework imports
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from hemisphere_backend.root_api import api_root

# local imports
from users import urls as UserUrls
from surveys import urls as SurveyUrls

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
    path('users/token/refresh/',TokenRefreshView.as_view() ,name='refresh-token')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)