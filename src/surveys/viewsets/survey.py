# django and python imports
import re
import boto3
from django.conf import settings

# rest framework imports

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# local imports
from surveys.models import *
from surveys.serializers import *
from surveys.utils import formatter

from utils import responses
from utils import permissions as custom_permissions
from surveys.serializers import QuestionSerializer,SurveySerializer
from rest_framework.response import Response

# bucket_name = settings.AWS_SECRET_BUCKET_NAME
# bucket_url = settings.AWS_BUCKET_URL

# session = boto3.session.Session()

# client_s3 = session.client(
#     's3',
#     region_name = settings.AWS_REGION_NAME,
#     aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
# )


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def get_permissions(self):
        if self.action in [
            "list",
            "create",
            "update",
            "partial_update",
            "delete",
            "destroy",
            "addQuestionToSurvey",
            "deleteQuestionsFromSurvey",
            "deleteDataCollectorsFromSurvey",
            "uploadFilesForSurvey",
        ]:
            permission_classes = [custom_permissions.IsAdmin]
        elif self.action in ["retrieve"]:
            permission_classes = [
                custom_permissions.IsAdmin | custom_permissions.IsDataCollector
            ]
        elif self.action in ["answerSurvey"]:
            permission_classes = [custom_permissions.IsDataCollector]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    """
        Get Surveys endpoint
    """

    def list(self, request, format=None):
        surveys = Survey.objects.all()

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the survey data",
            formatter.multipleSurveyFormatter(surveys),
        )

    """
        Get A Survey By Id
    """

    def retrieve(self, request, format=None, pk=None):
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey not Found")

        return responses.SuccessResponseHandler(
            True,
            "Successfully found the survey data",
            formatter.singleSurveyWithQuestions(checkSurvey[0]),
        )

    """
        Create Survey endpoint
    """

    def create(self, request, format=None):
        # checks all the required fields
        if (
            not "name"
            or not "status"
            or not "description"
            or not "project_id"
            or not "questions" in request.data.keys()
        ):
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks if the project exists
        checkProject = Project.objects.filter(pk=request.data["project_id"])
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project not Found")

        # checks the stauts is the correct way
        if request.data["status"] not in ["ACTIVE", "INACTIVE"]:
            return responses.BadRequestErrorHandler("status must be ACTIVE OR INACTIVE")

        # checks that the questions attribute is a list
        if type(request.data["questions"]) is not list:
            return responses.BadRequestErrorHandler("questions must be an array")

        # checks if questions is not empty
        if len(request.data["questions"]) == 0:
            return responses.BadRequestErrorHandler("questions can not be empty")
        # payload
        data={
            "project":request.data['project_id'],
            "name":request.data["name"],
            "description":request.data["description"],
            "status":request.data["status"],}
        
        serializer = SurveySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #return Response(serializer.data)
    
        # creates the survey
        # createdSurvey = Survey.objects.create(
        #     project=checkProject[0],
        #     name=request.data["name"],
        #     description=request.data["description"],
        #     status=request.data["status"],
        # )
        # print(request.data['questions'])
        # request.data['questions'] is a list .Loop through it .
        for question in request.data["questions"]:
        #     hasMultiple = False
        #     isDependent = False
        #     depQuestion = None
        #     title = ""
        #     isRequired = True
        #     questionType = ""
        #     questionOptions = None
        #     audioURL = None
        #     videoURL = None
        #     imageURL = None
        #     category = Category.objects.get(id=question["category_id"])
        #     language = Language.objects.get(id=question["language_id"])

            if type(question) is not dict:
                return responses.BadRequestErrorHandler(
                    "All question elements must be an object"
                )
            if len(question) == 0:
                return responses.BadRequestErrorHandler(
                    "Each Question must be non-empty"
                )
            if not "title" or not "type" in question.keys():
                return responses.BadRequestErrorHandler(
                    "All required fields for a question must be input"
                )

            if question["type"] not in ["CHOICE", "OPEN", "MEDIA"]:
                return responses.BadRequestErrorHandler(
                    "question types must be CHOICE, MEDIA or OPEN"
                )

            title = question["title"]
            questionType = question["type"]

            if question["type"] == "CHOICE":
                # checks the data if the question type is choice
                # checks if option is in questions dict
                if not "options" in question.keys():
                    return responses.BadRequestErrorHandler(
                        "All required fields for a question must be input"
                    )
                if len(question["options"]) == 0:
                    return responses.BadRequestErrorHandler(
                        "options is required for question type CHOICE"
                    )
                for option in question["options"]:
                    if type(option) != str:
                        return responses.BadRequestErrorHandler(
                            "question options must be strings"
                        )
                questionOptions = question["options"]

            if "isDependent" in question.keys() and question["isDependent"] == True:
                if not isinstance(question["isDependent"], bool):
                    return responses.BadRequestErrorHandler(
                        "question isDependent must be boolean"
                    )
                if not "depQuestion" in question.keys():
                    return responses.BadRequestErrorHandler(
                        "dependent question must have depQuestion"
                    )
                if not isinstance(question["depQuestion"], dict):
                    return responses.BadRequestErrorHandler(
                        "question depQuestion must be a dict"
                    )
                if not "title" in question["depQuestion"].keys():
                    return responses.BadRequestErrorHandler(
                        "question depQuestion must have title"
                    )
                checkPreviousQuestion = Question.objects.filter(
                    title=question["depQuestion"]["title"], survey=createdSurvey
                )
                if not checkPreviousQuestion.exists():
                    return responses.BadRequestErrorHandler(
                        "The previous question was not found"
                    )

                if checkPreviousQuestion[0].type == "CHOICE":
                    if not "value" in question["depQuestion"].keys():
                        return responses.BadRequestErrorHandler(
                            "question depQuestion must have value for question type CHOICE"
                        )

                    if not checkPreviousQuestion.filter(
                        options__contains=[question["depQuestion"]["value"]]
                    ).exists():
                        return responses.BadRequestErrorHandler(
                            "value in question depQuestion not in question choices"
                        )

                    isDependent = True
                    depQuestion = {
                        "id": checkPreviousQuestion[0].pk,
                        "value": question["depQuestion"]["value"],
                    }
                else:
                    value = None
                    if question["depQuestion"]["value"] and isinstance(
                        question["depQuestion"]["value"], str
                    ):
                        value = question["depQuestion"]["value"]

                    isDependent = True
                    depQuestion = {"id": checkPreviousQuestion[0].pk, "value": value}

            if "hasMultipleAnswers" in question.keys():
                if not isinstance(question["hasMultipleAnswers"], bool):
                    return responses.BadRequestErrorHandler(
                        "question hasMultipleAnswers must be boolean"
                    )
                hasMultiple = question["hasMultipleAnswers"]
            if "isRequired" in question.keys():
                if not isinstance(question["isRequired"], bool):
                    return responses.BadRequestErrorHandler(
                        "question isRequired must be boolean"
                    )
                isRequired = question["isRequired"]

            question_serializer = QuestionSerializer(data=question)
            if question_serializer.is_valid(raise_exception=True):
                question_serializer.save()
                result={"survey":serializer.data,
                        "question":question_serializer.data}
                return Response(result)
            # Question.objects.create(
            #     survey=createdSurvey,
            #     title=title,
            #     category=category,
            #     language=language,
            #     hasMultipleAnswers=hasMultiple,
            #     isRequired=isRequired,
            #     type=questionType,
            #     options=questionOptions,
            #     audioURL=audioURL,
            #     videoURL=videoURL,
            #     imageURL=imageURL,
            #     isDependent=isDependent,
            #     depQuestion=depQuestion,
            # )
           

        # checks if the project exists
        return responses.SuccessResponseHandler(
            True,
            "Successfully created a survey",
            # None
            formatter.singleSurveyWithQuestions(createdSurvey),
        )

    """
        Edit Survey Endpoint
    """

    def update(self, request, format=None, pk=None):
        # checks if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey not Found")

        # checks all the required fields
        if (
            not "name"
            or not "status"
            or not "description"
            or not "project_id"
            or not "questions" in request.data.keys()
        ):
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks if the project exists
        checkProject = Project.objects.filter(pk=request.data["project_id"])
        if not checkProject.exists():
            return responses.BadRequestErrorHandler("Project not Found")

        # checks the stauts is the correct way
        if request.data["status"] not in ["ACTIVE", "INACTIVE"]:
            return responses.BadRequestErrorHandler("status must be ACTIVE OR INACTIVE")

        # checks if questions is not empty
        if len(request.data["questions"]) == 0:
            return responses.BadRequestErrorHandler("questions can not be empty")

        # updates the survey
        checkSurvey.update(
            project=checkProject[0],
            name=request.data["name"],
            description=request.data["description"],
            status=request.data["status"],
        )

        for question in request.data["questions"]:
            hasMultiple = False
            title = ""
            isRequired = True
            questionType = ""
            questionOptions = None
            audioURL = None
            videoURL = None
            imageURL = None

            if type(question) is not dict:
                return responses.BadRequestErrorHandler(
                    "All question elements must be an object"
                )
            if len(question) == 0:
                return responses.BadRequestErrorHandler(
                    "Each Question must be non-empty"
                )
            if not "title" or not "type" or not "id" in question.keys():
                return responses.BadRequestErrorHandler(
                    "All required fields for a question must be input"
                )

            if question["type"] not in ["CHOICE", "OPEN", "MEDIA"]:
                return responses.BadRequestErrorHandler(
                    "question types must be CHOICE, MEDIA or OPEN"
                )

            checkQuestion = Question.objects.filter(
                pk=question["id"], survey=checkSurvey[0]
            )

            if not checkQuestion.exists():
                return responses.BadRequestErrorHandler("question not found")

            title = question["title"]
            questionType = question["type"]

            if question["type"] == "CHOICE":
                # checks the data if the question type is choice
                # checks if option is in questions dict
                if not "options" in question.keys():
                    return responses.BadRequestErrorHandler(
                        "All required fields for a question must be input"
                    )
                if len(question["options"]) == 0:
                    return responses.BadRequestErrorHandler(
                        "options is required for question type CHOICE"
                    )
                for option in question["options"]:
                    if type(option) != str:
                        return responses.BadRequestErrorHandler(
                            "question options must be strings"
                        )
                questionOptions = question["options"]

            if "hasMultipleAnswers" in question.keys():
                if not isinstance(question["hasMultipleAnswers"], bool):
                    return responses.BadRequestErrorHandler(
                        "question hasMultipleAnswers must be boolean"
                    )
                hasMultiple = question["hasMultipleAnswers"]
            if "isRequired" in question.keys():
                if not isinstance(question["isRequired"], bool):
                    return responses.BadRequestErrorHandler(
                        "question isRequired must be boolean"
                    )
                isRequired = question["isRequired"]

            checkQuestion.update(
                survey=checkSurvey[0],
                title=title,
                category=question["category"],
                language=question["language"],
                hasMultipleAnswers=hasMultiple,
                isRequired=isRequired,
                type=questionType,
                options=questionOptions,
                audioURL=audioURL,
                videoURL=videoURL,
                imageURL=imageURL,
            )

        return responses.SuccessResponseHandler(
            True,
            "Successfully Edited the Survey",
            formatter.singleSurveyWithQuestions(checkSurvey[0]),
        )

    """
        Delete Survey Endpoint
    """

    def destroy(self, request, format=None, pk=None):
        # checks the survey with the id exists
        checkSurvey = Survey.objects.filter(pk=pk)

        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey does not exist")

        checkSurvey.delete()

        return responses.SuccessResponseHandler(True, "Survey Deleted", None)

    """
        Add Question to Survey
    """

    @action(detail=True, methods=["POST"])
    def addQuestionToSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)

        if not "questions" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey does not exist")

        allCreatedQuestions = []
        for question in request.data["questions"]:
            hasMultiple = False
            isDependent = False
            depQuestion = None
            title = ""
            isRequired = True
            questionType = ""
            questionOptions = None
            audioURL = None
            videoURL = None
            imageURL = None

            if type(question) is not dict:
                return responses.BadRequestErrorHandler(
                    "All question elements must be an object"
                )
            if len(question) == 0:
                return responses.BadRequestErrorHandler(
                    "Each Question must be non-empty"
                )
            if not "title" or not "type" in question.keys():
                return responses.BadRequestErrorHandler(
                    "All required fields for a question must be input"
                )

            if question["type"] not in ["CHOICE", "OPEN", "MEDIA"]:
                return responses.BadRequestErrorHandler(
                    "question types must be CHOICE , MEDIA or OPEN"
                )

            title = question["title"]
            questionType = question["type"]

            if question["type"] == "CHOICE":
                # checks the data if the question type is choice
                # checks if option is in questions dict
                if not "options" in question.keys():
                    return responses.BadRequestErrorHandler(
                        "All required fields for a question must be input"
                    )
                if len(question["options"]) == 0:
                    return responses.BadRequestErrorHandler(
                        "options is required for question type CHOICE"
                    )
                for option in question["options"]:
                    if type(option) != str:
                        return responses.BadRequestErrorHandler(
                            "question options must be strings"
                        )
                questionOptions = question["options"]

            if "isDependent" in question.keys() and question["isDependent"] == True:
                if not isinstance(question["isDependent"], bool):
                    return responses.BadRequestErrorHandler(
                        "question isDependent must be boolean"
                    )
                if not "depQuestion" in question.keys():
                    return responses.BadRequestErrorHandler(
                        "dependent question must have depQuestion"
                    )
                if not isinstance(question["depQuestion"], dict):
                    return responses.BadRequestErrorHandler(
                        "question depQuestion must be a dict"
                    )
                if not "title" in question["depQuestion"].keys():
                    return responses.BadRequestErrorHandler(
                        "question depQuestion must have title"
                    )
                checkPreviousQuestion = Question.objects.filter(
                    title=question["depQuestion"]["title"], survey=checkSurvey[0]
                )
                if not checkPreviousQuestion.exists():
                    return responses.BadRequestErrorHandler(
                        "The previous question was not found"
                    )

                if checkPreviousQuestion[0].type == "CHOICE":
                    if not "value" in question["depQuestion"].keys():
                        return responses.BadRequestErrorHandler(
                            "question depQuestion must have value for question type CHOICE"
                        )

                    if not checkPreviousQuestion.filter(
                        options__contains=[question["depQuestion"]["value"]]
                    ).exists():
                        return responses.BadRequestErrorHandler(
                            "value in question depQuestion not in question choices"
                        )

                    isDependent = True
                    depQuestion = {
                        "id": checkPreviousQuestion[0].pk,
                        "value": question["depQuestion"]["value"],
                    }
                else:
                    value = None
                    if question["depQuestion"]["value"] and isinstance(
                        question["depQuestion"]["value"], str
                    ):
                        value = question["depQuestion"]["value"]

                    isDependent = True
                    depQuestion = {"id": checkPreviousQuestion[0].pk, "value": value}

            if "hasMultipleAnswers" in question.keys():
                if not isinstance(question["hasMultipleAnswers"], bool):
                    return responses.BadRequestErrorHandler(
                        "question hasMultipleAnswers must be boolean"
                    )
                hasMultiple = question["hasMultipleAnswers"]
            if "isRequired" in question.keys():
                if not isinstance(question["isRequired"], bool):
                    return responses.BadRequestErrorHandler(
                        "question isRequired must be boolean"
                    )
                isRequired = question["isRequired"]

            createdQuestion = Question.objects.create(
                survey=checkSurvey[0],
                title=title,
                category=question["category"],
                language=question["language"],
                hasMultipleAnswers=hasMultiple,
                isRequired=isRequired,
                type=questionType,
                options=questionOptions,
                audioURL=audioURL,
                videoURL=videoURL,
                imageURL=imageURL,
                isDependent=isDependent,
                depQuestion=depQuestion,
            )

            allCreatedQuestions.append(createdQuestion)

        return responses.SuccessResponseHandler(
            True,
            "Added the questions to the survey",
            formatter.multipleQuestionFormatter(allCreatedQuestions),
        )

    """
        Upload files for survey
    """

    @action(detail=True, methods=["POST"])
    def uploadFilesForSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey doesn't exist.")

        # checks all questions for survey with type media
        checkAllQuestionForMedia = Question.objects.filter(
            survey=checkSurvey[0], type="MEDIA"
        )

        # checks all question for survey with type media and no files
        checkAllQuestionForMediaWoutFiles = Question.objects.filter(
            survey=checkSurvey[0],
            type="MEDIA",
            audioURL=None,
            imageURL=None,
            videoURL=None,
        )
        if not checkAllQuestionForMedia.exists():
            return responses.BadRequestErrorHandler(
                "no question with type media exists"
            )

        print(len(request.data.keys()))
        print(len(checkAllQuestionForMediaWoutFiles))
        # checks if the data input matches the questions with media type
        if len(request.data.keys()) < len(checkAllQuestionForMediaWoutFiles):
            return responses.BadRequestErrorHandler(
                "responses must match the questions with type MEDIA"
            )

        allowedAudioFiles = [
            "audio/ogg",
            "audio/mp3",
            "audio/wav",
            "audio/m4a",
            "audio/aac",
            "audio/wma",
            "audio/mpeg",
        ]
        allowedVideoFiles = [
            "video/mp4",
            "video/mov",
            "video/mkv",
            "video/avi",
            "video/gif",
            "video/flv",
        ]
        allowedImageFiles = [
            "image/png",
            "image/jpg",
            "image/jpeg",
            "image/bmp",
            "image/svg",
            "image/gif",
        ]

        for key in request.data.keys():
            separator = key.find("_")

            if separator == -1:
                return responses.BadRequestErrorHandler(
                    "format of all keys must be id_${type}"
                )

            id = key[: int(separator)]
            type = key[int(separator) + 1 :]

            try:
                id = int(id)
            except ValueError:
                return responses.BadRequestErrorHandler("all key ids must be integers")
            if type not in ["audio", "video", "image"]:
                return responses.BadRequestErrorHandler(
                    "all key types must be from audio, video and image"
                )
            value = request.data[key]

            if not hasattr(value, "content_type"):
                return responses.BadRequestErrorHandler("all values must be files")
            if type == "audio":
                print(value.content_type)
                if value.content_type not in allowedAudioFiles:
                    return responses.BadRequestErrorHandler("file type not allowed")
            if type == "video":
                if value.content_type not in allowedVideoFiles:
                    return responses.BadRequestErrorHandler("file type not allowed")
            if type == "image":
                if value.content_type not in allowedImageFiles:
                    return responses.BadRequestErrorHandler("file type not allowed")

            checkQuestion = Question.objects.filter(pk=id, survey=checkSurvey[0])
            if not checkQuestion.exists():
                return responses.BadRequestErrorHandler(
                    "question does not exist for the survey"
                )

            key = "question" + str(checkQuestion[0].pk) + str(value.name)
            client_s3.upload_fileobj(value.file, bucket_name, key)

            audioUrl = None
            videoUrl = None
            imageUrl = None

            url = bucket_url + "/" + key
            if type == "audio":
                audioUrl = url
            elif type == "video":
                videoUrl = url
            elif type == "image":
                imageUrl = url

            checkQuestion.update(
                audioURL=audioUrl, imageURL=imageUrl, videoURL=videoUrl
            )

        return responses.SuccessResponseHandler(
            True,
            "Successfully uploaded the files for the survey",
            formatter.singleSurveyWithQuestions(checkSurvey[0]),
        )

    """
        Delete Question from survey
    """

    @action(detail=True, methods=["PUT"])
    def deleteQuestionsFromSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey doesn't exist.")

        if not "questions" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        # checks that the questions attribute is a list
        if type(request.data["questions"]) is not list:
            return responses.BadRequestErrorHandler("questions must be an array")

        # checks if questions is not empty
        if len(request.data["questions"]) == 0:
            return responses.BadRequestErrorHandler("questions can not be empty")

        for question in request.data["questions"]:
            # checks that the questions attribute is a list
            if type(question) is not int:
                return responses.BadRequestErrorHandler("question ids must be integers")

            checkQuestion = Question.objects.filter(pk=question, survey=checkSurvey[0])
            if not checkQuestion.exists():
                return responses.BadRequestErrorHandler("All questions must be found.")

            checkQuestion.delete()

        return responses.SuccessResponseHandler(
            True,
            "Deleted the questions from the survey",
            formatter.singleSurveyWithQuestions(checkSurvey[0]),
        )

    """
        Add Data Collectors to survey endpoint
    """

    @action(detail=True, methods=["POST"])
    def addDataCollectorToSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey doesn't exist.")

        # checks all the required attributes
        if not "dataCollectors" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        if not isinstance(request.data["dataCollectors"], list):
            return responses.BadRequestErrorHandler("dataCollectors must be an array")

        if not request.data["dataCollectors"]:
            return responses.BadRequestErrorHandler(
                "dataCollectors array must not be empty"
            )

        checkDataCollectors = ExtendedUser.objects.filter(
            pk__in=request.data["dataCollectors"], role__role="Data-Collector"
        )

        if len(checkDataCollectors) != len(request.data["dataCollectors"]):
            return responses.BadRequestErrorHandler(
                "all data collectors were not found"
            )

        checkExisting = (
            checkSurvey[0]
            .dataCollectors.all()
            .filter(id__in=request.data["dataCollectors"])
        )
        if checkExisting.exists():
            return responses.BadRequestErrorHandler(
                "All data collectors to be added must not be assigned to the event"
            )

        for user in checkDataCollectors:
            checkSurvey[0].dataCollectors.add(user)

        return responses.SuccessResponseHandler(
            True,
            "Successfully added data collectors to the survey",
            formatter.singleSurveyFormatter(checkSurvey[0]),
        )

    """
        Remove data collectors from survey
    """

    @action(detail=True, methods=["POST"])
    def deleteDataCollectorsFromSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey doesn't exist.")

        # checks all the required attributes
        if not "dataCollectors" in request.data.keys():
            return responses.BadRequestErrorHandler("All required fields must be input")

        if not isinstance(request.data["dataCollectors"], list):
            return responses.BadRequestErrorHandler("dataCollectors must be an array")

        if not request.data["dataCollectors"]:
            return responses.BadRequestErrorHandler(
                "dataCollectors array must not be empty"
            )

        checkDataCollectors = ExtendedUser.objects.filter(
            pk__in=request.data["dataCollectors"], role__role="Data-Collector"
        )

        if len(checkDataCollectors) != len(request.data["dataCollectors"]):
            return responses.BadRequestErrorHandler(
                "all data collectors were not found"
            )

        checkExisting = (
            checkSurvey[0]
            .dataCollectors.all()
            .filter(id__in=request.data["dataCollectors"])
        )

        if len(checkExisting) != len(checkDataCollectors):
            return responses.BadRequestErrorHandler(
                "all data collectors were not assigned to the survey"
            )

        for user in checkExisting:
            checkSurvey[0].dataCollectors.remove(user)

        return responses.SuccessResponseHandler(
            True,
            "Successfully removed the data collectors from the survey",
            formatter.singleSurveyFormatter(checkSurvey[0]),
        )

    """
        Answer survey for data collectors
    """

    @action(detail=True, methods=["PUT"])
    def answerSurvey(self, request, format=None, pk=None):
        # check if the survey exists
        checkSurvey = Survey.objects.filter(pk=pk)
        if not checkSurvey.exists():
            return responses.BadRequestErrorHandler("Survey doesn't exist.")

        # check all required fields
        if not "answers" or not "location" in request.data.keys():
            return responses.BadRequestErrorHandler(
                "All required fields must be input."
            )

        # checks the type is correct
        if not isinstance(request.data["answers"], list):
            return responses.BadRequestErrorHandler("answers must be an array")
        if len(request.data["answers"]) == 0:
            return responses.BadRequestErrorHandler("answers must not be empty")

        # fetches all questions for the survey
        allQuestions = Question.objects.filter(survey=checkSurvey[0])
        if not allQuestions.exists():
            return responses.BadRequestErrorHandler("no questions exist for the survey")

        # checks the length of the questions that are input in the request body to be accurate
        if len(request.data["answers"]) < len(allQuestions.filter(isRequired=True)):
            return responses.BadRequestErrorHandler(
                "all required questions must be answered"
            )

        if len(request.data["answers"]) > len(allQuestions.filter()):
            return responses.BadRequestErrorHandler(
                "questions to be answered must not exceed the actual questions"
            )

        for question in request.data["answers"]:
            # checks all required fields are input
            if not "question_id" or not "response" in question:
                return responses.BadRequestErrorHandler(
                    "every question must have a question_id and response property"
                )

            # makes sure the question has the correct properties
            if not isinstance(question["question_id"], int):
                return responses.BadRequestErrorHandler("all question ids must be int")

            if not isinstance(question["response"], list):
                return responses.BadRequestErrorHandler(
                    "all response properties must be an array"
                )

            if len(question["response"]) < 1:
                return responses.BadRequestErrorHandler("response can not be empty")

            # checks the question with the id exists for the survey
            checkQuestion = Question.objects.filter(
                pk=question["question_id"], survey=checkSurvey[0]
            )
            if not checkQuestion.exists():
                return responses.BadRequestErrorHandler(
                    "question id for the survey does not exist"
                )

            if (
                len(question["response"]) > 1
                and checkQuestion[0].hasMultipleAnswers == False
            ):
                return responses.BadRequestErrorHandler(
                    "question not allowed to have multiple answers"
                )

            # checks the question answer is correct for the type
            if checkQuestion[0].type == "CHOICE":
                for response in question["response"]:
                    if not checkQuestion.filter(options__contains=[response]).exists():
                        return responses.BadRequestErrorHandler(
                            "all answers for type choice must be in question options"
                        )

            # checks a dependent condition and the value
            if checkQuestion[0].isDependent == True:
                checkDepQuestion = next(
                    (
                        answer
                        for answer in request.data["answers"]
                        if answer["question_id"] == checkQuestion[0].depQuestion["id"]
                        and answer["response"][0]
                        == checkQuestion[0].depQuestion["value"]
                    ),
                    None,
                )
                if checkDepQuestion == None:
                    return responses.BadRequestErrorHandler(
                        "dependepent question value not correct"
                    )

        [
            QuestionAnswer.objects.create(
                question=Question.objects.get(pk=answer["question_id"]),
                responses=answer["response"],
                location=request.data["location"],
            )
            for answer in request.data["answers"]
        ]

        return responses.SuccessResponseHandler(
            True,
            "Successfully registered the answer for the survey.",
            formatter.singleSurveyFormatter(checkSurvey[0]),
        )
