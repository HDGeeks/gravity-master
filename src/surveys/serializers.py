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
    class Meta:
        model = Survey
        fields = "__all__"

   


class QuestionSerializer(serializers.ModelSerializer):
    # category = serializers.CharField()

    class Meta:
        model = Question
        fields = "__all__"

    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     #category_name = category_data.get('name')
    #     category = Category.objects.get_or_create(name=category_data)
    #     print("================================",category_data)
    #     print("================================",category)
        
        
        # validated_data['category'] = category.pk
        # question = Question.objects.create(**validated_data)
        # return question
