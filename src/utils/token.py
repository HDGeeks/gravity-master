# Packages needed for checking the request header token
import jwt
from datetime import datetime

from users.models import ExtendedUser, Role
from utils import responses


# method that checks token of admins
def checkAdminToken(headers):
    if ("Authorization") not in headers:
        return responses.BadRequestErrorHandler("Authorization token is required")
    jwtToken = headers["Authorization"]
    return checkAdminFromToken(jwtToken)


# method that checks token of data collectors
def checkDataCollectorToken(headers):
    if ("Authorization") not in headers:
        return responses.BadRequestErrorHandler("Authorization token is required")
    jwtToken = headers["Authorization"]
    return checkDataCollectorFromToken(jwtToken)


# check admin from token
def checkAdminFromToken(token):
    # extracts the token
    index = token.find(" ")
    token = token[index:]

    # decodes the JWT token
    decodedToken = jwt.decode(
        token, options={"verify_signature": False}, algorithms=["HS256"]
    )
    # checks the type of the token is access
    if decodedToken["token_type"] != "access":
        return False
    if datetime.now() > datetime.fromtimestamp(decodedToken["exp"]):
        return False

    # checks the role exists
    checkRole = Role.objects.filter(role="Admin")
    if not checkRole.exists():
        return False

    # checks the user with the rule
    user = ExtendedUser.objects.filter(
        pk=decodedToken["user_id"], role__id=checkRole[0].pk
    )
    if user.exists():
        return True
    else:
        return False


# check data collector from token
def checkDataCollectorFromToken(token):
    # extracts the token
    index = token.find(" ")
    token = token[index:]

    # decodes the JWT token
    decodedToken = jwt.decode(
        token, options={"verify_signature": False}, algorithms=["HS256"]
    )
    # checks the type of the token is access
    if decodedToken["token_type"] != "access":
        return False
    if datetime.now() > datetime.fromtimestamp(decodedToken["exp"]):
        return False

    # checks the role exists
    checkRole = Role.objects.filter(role="Data-Collector")
    if not checkRole.exists():
        return False

    # checks the user with the rule
    user = ExtendedUser.objects.filter(
        pk=decodedToken["user_id"], role__id=checkRole[0].pk
    )
    if user.exists():
        return True
    else:
        return False


# returns the user from the token
def getUserFromToken(token):
    index = token.find(" ")
    token = token[index:]

    decodedToken = jwt.decode(
        token, options={"verify_signature": False}, algorithms=["HS256"]
    )
    # checks the type of the token is access
    if decodedToken["token_type"] != "access":
        return False

    user = ExtendedUser.objects.filter(pk=decodedToken["user_id"])

    return (user[0], user[0].pk)
