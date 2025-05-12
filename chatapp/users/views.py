import logging
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer
from core.utils import error_handler


logger = logging.getLogger(__name__)


@api_view(['POST'])
@error_handler
def register_user(request):
    if request.method == 'POST':
        data = request.data  # username, email, password
        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

            logger.info(f"User {user.username} registered successfully.")


            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'User created successfully',
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)

        logger.error(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


# @api_view(['POST'])
# @error_handler
# def login_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#
#     logger.info(f"Login attempt for username: {username}")
#
#     user = authenticate(request, username=username, password=password)
#
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         logger.info(f"User {username} logged in successfully.")
#
#         return Response({
#             "message": "Login successful",
#             "access_token": str(refresh.access_token),
#             "refresh_token": str(refresh),
#         }, status=status.HTTP_200_OK)
#     else:
#         logger.warning(f"Login failed for username: {username}")
#
#         return Response({
#             "error": "Invalid credentials"
#         }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@error_handler
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    logger.info(f"Login attempt for username: {username}")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        user_data = CustomUserSerializer(user).data

        refresh = RefreshToken.for_user(user)
        logger.info(f"User {username} logged in successfully.")

        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": user_data
        }, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Login failed for username: {username}")
        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@error_handler
def logout_user(request):
    refresh_token = request.data.get("refresh_token")

    try:
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        logger.info(f"User logged out successfully. Refresh token blacklisted.")

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

    except InvalidToken:
        logger.warning("Invalid refresh token provided.")
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@error_handler
@permission_classes([IsAuthenticated])
def user_detail(request):
    print("DEBUG - user:", request.user)
    serializer = CustomUserSerializer(request.user)
    user = request.user
    if request.user.is_authenticated:
        print("Authenticated as:", request.user.username)
    else:
        print("User is not authenticated!")
    # return Response(serializer.data)
    return JsonResponse({
        "user_id": user.id,
        "username": user.username,
    })

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
