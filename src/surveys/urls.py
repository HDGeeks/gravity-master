from posixpath import basename
from rest_framework import routers

# local imports
from .viewsets import (
    customer,
    project,
    survey
)

# define all urls related to the users app
router = routers.DefaultRouter()

router.register("customer",customer.CustomerViewSet,basename="customers")
router.register("project",project.ProjectViewSet,basename="projects")
router.register("survey",survey.SurveyViewSet, basename="surveys")

urlpatterns = router.urls