# django models

# rest framework imports
from rest_framework import serializers

# local imports
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "description", "location", "contact"]


class ProjectSerializer(serializers.ModelSerializer):
  
    #customer= serializers.StringRelatedField(many=True)
    #customer = CustomerSerializer(many=True ,read_only=True)
 
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


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ["id", "project", "name", "description", "status"]
        # fields='__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]
