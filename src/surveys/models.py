from django.db import models
from django.contrib.postgres.fields import ArrayField

# import PlainLocationfield model field
from location_field.models.plain import PlainLocationField

from users.models import ExtendedUser

# Create your models here.
class Customer(models.Model):

    name = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

class Project(models.Model):

    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, unique = True)
    description = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300,default="")
    noOfDataCollectors = models.IntegerField(default=0)
    budget = models.FloatField(default=0)

class Survey(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE','ACTIVE'),
        ('INACTIVE','INACTIVE')
    )

    project = models.ForeignKey(Project, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,default="")
    dataCollectors = models.ManyToManyField(ExtendedUser)

class Question(models.Model):

    QUESTION_TYPES = (
        ('CHOICE','CHOICE'),
        ('OPEN','OPEN'),
        ('MEDIA','MEDIA')
    )

    survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
    title = models.CharField(max_length=500)
    hasMultipleAnswers = models.BooleanField(default=False)
    isDependent = models.BooleanField(default=False)
    depQuestion = models.JSONField(null = True)
    isRequired = models.BooleanField(default=True)
    type = models.CharField(choices=QUESTION_TYPES,null=False,max_length=30,)
    options = ArrayField(null=True,base_field=models.CharField(max_length=300, blank=True))
    audioURL = models.URLField(null=True)
    imageURL = models.URLField(null=True)
    videoURL = models.URLField(null=True)

class QuestionAnswer(models.Model):

    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    responses = ArrayField(null=False,base_field=models.CharField(max_length= 300, blank=True))
    location = PlainLocationField(based_fields=['city'],zoom=7,default="")