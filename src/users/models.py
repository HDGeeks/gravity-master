from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ExtendedUser(AbstractUser):

    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255,verbose_name='email')
    email_verified = models.BooleanField(default=False)
    middle_name = models.CharField(max_length=255)
    role = models.ForeignKey('Role',on_delete= models.CASCADE,null=True)

    def __str__(self):
        return f"{self.email}"

class Role(models.Model):

    ROLE_CHOICES = (
        ('Admin','Admin'),
        ('Data-Collector','Data-Collector')
    )

    role = models.CharField(max_length=50,choices=ROLE_CHOICES, unique = True)

    def __str__(self):
        return self.role
