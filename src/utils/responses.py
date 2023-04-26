"""
    This file defines custom response handlers i.e errors or success responses, that can be used in all files
"""

# restframework imports
from rest_framework import status
from rest_framework.response import Response

# response for common bad request response with status code 400
def BadRequestErrorHandler(message):
    return Response({
        "message":message
    },
    status.HTTP_400_BAD_REQUEST
    )

# response for common failed login attempt response with status code 401
def LoginErrorHandler():
    return Response({"message":"Invalid credentials"},status.HTTP_401_UNAUTHORIZED)

# response for commoin validation realted error responses
def ValidationErrorHandler(message):
    return Response({
        "message":message
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    
# response for common success responses
def SuccessResponseHandler(success,message,data):
    return Response({
        "success":success,
        "message":message,
        "data":data
    })

# response for common deleted responses
def NotFoundResponseHandler(message):
    return Response({
        "message":message
    },
    status.HTTP_404_NOT_FOUND
    )