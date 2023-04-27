
from users.serializers import SignInSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from users.models import ExtendedUser,Role
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from utils import responses 




@api_view(['post'])
def admin_sign_in(request):
    serializer = SignInSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    username = request.data['email']
    password = request.data['password']
  
    check_if_user_is_admin= ExtendedUser.objects.filter(username=username).filter(role=1).distinct()
 
    if not check_if_user_is_admin:
        return Response({
        'detail': 'User is not admin .',
        'email': user.get_username()
    }, status=status.HTTP_200_OK)


    user = authenticate(request=request,username=username, password=password)
    
    if not user:
        return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    
    return responses.SuccessResponseHandler(
        True,
        "Succesfully logged in",
        {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'email': user.get_username()
    })


