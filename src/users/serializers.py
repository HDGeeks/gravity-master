# django models 

# rest framework imports
from rest_framework import serializers

# local imports
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtendedUser
        fields = ('id','first_name','last_name','username','email','phone')

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtendedUser
        fields = ('id','role')