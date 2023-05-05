from surveys.serializers import SurveySerializer
from surveys.models import Survey
from rest_framework.viewsets import ModelViewSet


class NewSurvey(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
