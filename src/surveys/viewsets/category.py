from requests import Response
from rest_framework.viewsets import ModelViewSet
from surveys.serializers import QuestionSerializer,CategorySerializer
from surveys.models import Question,Category
from utils import permissions as custom_permissions
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=custom_permissions.IsAdmin


class QuestionByCategoryAndLanguage(ModelViewSet):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer
    http_method_names=['GET']
    permission_classes=[IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        # Check if category query parameter is present and filter by category if it is
        category = request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)

         # Check if survey_id query parameter is present and filter by survey id if it is
        survey_id = request.query_params.get('survey', None)
        if survey_id is not None:
            queryset = queryset.filter(survey__id=survey_id)

         # Check if survey_id query parameter is present and filter by survey id if it is
        language_id= request.query_params.get('language', None)
        if language_id is not None:
            queryset = queryset.filter(language__id=language_id)


        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)