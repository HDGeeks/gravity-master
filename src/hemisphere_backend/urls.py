from django.contrib import admin
from django.urls import path,include

# rest framework imports
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

# local imports
from users import urls as UserUrls
from surveys import urls as SurveyUrls

router = routers.DefaultRouter()

urlpatterns = [
    # defines the default django admin url
    path('admin/', admin.site.urls),

    # defines the app urls created
    path(r'users/',include(UserUrls)),
    path(r'surveys/',include(SurveyUrls)),

    # defines the refresh token and common urls
    path('users/token/refresh/',TokenRefreshView.as_view())
]