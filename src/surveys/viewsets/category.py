from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from surveys.serializers import QuestionSerializer, CategorySerializer
from surveys.models import Question, Category
from utils import permissions as custom_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from surveys.models import Survey
from surveys.utils.formatter import multipleQuestionFormatter
from utils import responses


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
        # Step 1: Retrieve the category_id and survey_id from the query parameters
        category_name = request.query_params.get("category")
        survey_id = request.query_params.get("survey")
     

        # Step 2: Get the queryset for the Question model
        queryset = self.queryset

        # Step 3: If no category_id and survey_id are provided, return all questions
        
        if not category_name and not survey_id:
            return responses.SuccessResponseHandler(
            True,
            "Successfully found the survey data",
            multipleQuestionFormatter(queryset),
        )
            
           
        
        elif survey_id and not category_name:
            queryset = queryset.filter(survey__id=survey_id)
            return responses.SuccessResponseHandler(
            True,
            "Successfully found the survey data",
            multipleQuestionFormatter(queryset),
        )
        
        else:

            
            try:
                check_category_existence = (
                    queryset.filter(category__name=category_name).values("category").exists()
                )
            except Exception as e:
                return Response(str(e), status=404)

            if not check_category_existence:
                return Response(
                    "There are no questions for the provided category.", status=400
                )

            # Step 7: Filter the queryset by survey_id and category_id
            if survey_id:
                queryset = queryset.filter(survey__id=survey_id)
            if category_name:
                queryset = queryset.filter(category__name=category_name)

            return responses.SuccessResponseHandler(
            True,
            "Successfully found the survey data",
            multipleQuestionFormatter(queryset),
        )

          









# # Step 4: If a survey_id is provided, find the survey and retrieve the list of related category IDs
            # try:
            #     unit_survey = Survey.objects.filter(id=survey_id).values("categories__id")
            #     categories_list = []

            #     for survey in unit_survey:
            #         categories_list.append(survey["categories__id"])

            # except Exception as e:
            #     return Response(str(e), status=404)

            # print(category_id)
            # print(categories_list)

            # # Step 5: If a category_id is provided, check if it exists in the categories_list from step 4
            # if int(category_id) not in categories_list:
            #     return Response(
            #         "The passed category does not belong to this survey.", status=400
            #     )

            # Step 6: Check if the provided category_id exists in the Question model