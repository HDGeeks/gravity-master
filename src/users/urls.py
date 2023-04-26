from rest_framework import routers

# local imports
from .viewsets import (
    user,
    admin,
    dataCollector
)

# define all urls related to the users app
router = routers.DefaultRouter()

router.register("user",user.UserViewSet,basename ="users")
router.register("admin",admin.AdminViewSet,basename = "admins")
router.register("data-collector",dataCollector.DataCollectorViewset,basename = "data-collectors")

urlpatterns = router.urls
