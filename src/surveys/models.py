from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Subquery, OuterRef
from users.models import Role

# import PlainLocationfield model field
from location_field.models.plain import PlainLocationField

from users.models import ExtendedUser

# Create your models here.


# Create your models here.
class CreationTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # ordering = ["created_at"]


class Category(CreationTimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Language(CreationTimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name


class Customer(CreationTimeStamp):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "customers"
        # unique_together = ('name', 'contact')
        indexes = [
            models.Index(fields=["name"], name="customer_name_idx"),
        ]

    def __str__(self):
        return self.name


class Project(CreationTimeStamp):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300, default="")
    noOfDataCollectors = models.IntegerField(default=0)
    budget = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Projects"
        # unique_together = ('name', 'customer')
        # indexes = [
        #     models.Index(fields=['name'], name='customer_name_idx'),
        #     models.Index(fields=['customer'], name='customer_id_idx'),
        #     ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Project(name={self.name}, customer={self.customer}, date={self.date}, budget={self.budget})"


class Survey(CreationTimeStamp):
    STATUS_CHOICES = (("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE"))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category", blank=True)
    language = models.ForeignKey(
        "Language", on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="")
    dataCollectors = models.ManyToManyField(ExtendedUser)

    # limit_choices_to={'role': 'data_collector'}

    class Meta:
        verbose_name_plural = "Surveys"
        # unique_together = ('name', 'project')
        indexes = [
            models.Index(fields=["name"], name="project"),
            models.Index(fields=["project"], name="project_id_idx"),
            models.Index(fields=["language"], name="survey_language_idx"),
        ]

    def __str__(self):
        return self.name


class Question(CreationTimeStamp):
    QUESTION_TYPES = (("CHOICE", "CHOICE"), ("OPEN", "OPEN"), ("MEDIA", "MEDIA"))

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, null=False, blank=False
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=500)
    hasMultipleAnswers = models.BooleanField(default=False)
    isDependent = models.BooleanField(default=False)
    depends_on = models.ManyToManyField("self", null=True, blank=True)
    depQuestion = models.JSONField(null=True)
    isRequired = models.BooleanField(default=True)
    type = models.CharField(
        choices=QUESTION_TYPES,
        null=False,
        max_length=30,
    )
    options = ArrayField(
        null=True, base_field=models.CharField(max_length=300, blank=True)
    )
    audioURL = models.URLField(null=True)
    imageURL = models.URLField(null=True)
    videoURL = models.URLField(null=True)

    class Meta:
        verbose_name_plural = "Questions"
        # unique_together = ('survey', 'title')
        indexes = [
            models.Index(fields=["title"], name="title_idx"),
            models.Index(fields=["survey"], name="survey_id_idx"),
            # models.Index(fields=["category"], name="category_id_idx"),
        ]

    def __str__(self) -> str:
        if self.category:
            return f"{self.title} ({self.category.name})"
        else:
            return self.title


class QuestionAnswer(CreationTimeStamp):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    responses = ArrayField(
        null=False, base_field=models.CharField(max_length=300, blank=True)
    )
    location = PlainLocationField(based_fields=["city"], zoom=7, default="")

    class Meta:
        verbose_name_plural = "QuestionAnswers"
        indexes = [
            models.Index(fields=["question"], name="question_id_idx"),
            models.Index(fields=["category"], name="category_id_idx"),
        ]

    def __str__(self) -> str:
        return self.question
