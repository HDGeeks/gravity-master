# django models

# rest framework imports
from rest_framework import serializers

# local imports
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "description", "location", "contact"]


class ProjectSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Project
        fields = [
            "id",
            "customer",
            "name",
            "description",
            "date",
            "location",
            "noOfDataCollectors",
            "budget",
        ]


# class SurveySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Survey
#         #fields = ["id", "project", "name", "description", "status"]
#         fields='__all__'


class SurveySerializer(serializers.ModelSerializer):
    # language = serializers.CharField()
    # categories = serializers.ListField(child=serializers.CharField())
    # dataCollectors = serializers.PrimaryKeyRelatedField(queryset=ExtendedUser.objects.all(), many=True)

    class Meta:
        model = Survey
        fields = "__all__"

    def create(self, validated_data):
        data_collectors_data = validated_data.pop("dataCollectors", [])
        language_name = validated_data.pop("language", None)
        if language_name:
            language, created = Language.objects.get_or_create(name=language_name)
            validated_data["language"] = language
            
        categories_data = validated_data.pop("categories", [])
        survey = Survey.objects.create(**validated_data)

        for category_name in categories_data:
            category, created = Category.objects.get_or_create(name=category_name)
            survey.categories.add(category)

        for data_collector in data_collectors_data:
            survey.dataCollectors.add(data_collector)

        return survey




class QuestionSerializer(serializers.ModelSerializer):
    #category = serializers.CharField()

    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        category_name = validated_data.pop("category", None)
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            validated_data["category"] = category
        question = Question.objects.create(**validated_data)
        return question




