from rest_framework import routers
from django.urls import path

# local imports
from .viewsets import (
    user,
    admin,
    dataCollector
)
from .views import admin_sign_in
# define all urls related to the users app
router = routers.DefaultRouter()

router.register("user",user.UserViewSet,basename ="users")
router.register("admin",admin.AdminViewSet,basename = "admins")
router.register("data-collector",dataCollector.DataCollectorViewset,basename = "data-collectors")

urlpatterns = [
    path('new-admin-sign-in',admin_sign_in,name='new-admin-sign-in'),
    
    
]

urlpatterns += router.urls
