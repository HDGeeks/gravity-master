from django.contrib import admin
from .models import (
    Customer,
    Project,
    Survey,
    Category,
    Language,
    Question,
    QuestionAnswer,
)

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "location", "contact")
    search_fields = ("name", "location", "contact")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "name",
        "description",
        "date",
        "location",
        "noOfDataCollectors",
        "budget",
    )
    search_fields = ("name", "customer__name")
    list_filter = ("customer",)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "name", "description", "status")
    search_fields = ("name", "project__name")
    list_filter = ("project",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "survey",
        "category",
        "language",
        "title",
        "hasMultipleAnswers",
        "isDependent",
        "isRequired",
        "type",
    )
    search_fields = ("title", "survey__name")
    list_filter = ("survey", "category", "language", "type")


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "createdAt", "location")
    search_fields = ("question__title",)
    list_filter = ("question",)
