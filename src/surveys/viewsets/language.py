from surveys.models import Language
from surveys.serializers import LanguageSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from utils import permissions as custom_permissions


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
    #permission_classes = [custom_permissions.IsAdmin]
