from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from surveys.serializers import QuestionSerializer, CategorySerializer
from surveys.models import Question, Category
from utils import permissions as custom_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes=custom_permissions.IsAdmin


class QuestionByCategoryAndLanguage(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ["get"]
    # permission_classes=[IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        category_id = request.query_params.get("category")
        print(category_id)
        survey_id = request.query_params.get("survey")
        language_id = request.query_params.get("language")

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if survey_id:
            queryset = queryset.filter(survey__id=survey_id)
        if language_id:
            queryset = queryset.filter(language__id=language_id)
        if category_id and survey_id and language_id:
            queryset = queryset.filter(
                category__id=category_id, survey__id=survey_id, language__id=language_id
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
