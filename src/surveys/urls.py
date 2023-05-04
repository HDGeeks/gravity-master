from posixpath import basename
from rest_framework import routers
from .viewsets.category import CategoryViewSet, QuestionByCategoryAndLanguage
from .viewsets.language import LanguageViewSet
from .viewsets.survey2 import NewSurvey


# local imports
from .viewsets import customer, project, survey, category

# define all urls related to the users app
router = routers.DefaultRouter()

router.register("customer", customer.CustomerViewSet, basename="customers")
router.register("project", project.ProjectViewSet, basename="projects")
router.register("survey", survey.SurveyViewSet, basename="surveys")
router.register("categories", CategoryViewSet, basename="category")
router.register(
    "questions-category", QuestionByCategoryAndLanguage, basename="questions-category"
)
router.register("language", LanguageViewSet, basename="language")
router.register("new-sur", NewSurvey, basename="new-sur")

urlpatterns = router.urls
