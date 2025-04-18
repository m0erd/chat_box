# import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer

from core.utils import error_handler


# logger = logging.getLogger(__name__)


@api_view(['POST'])
@error_handler
def register_user(request):
    if request.method == 'POST':
        data = request.data  # username, email, password
        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

#             logger.info(f"User {user.username} registered successfully.")


            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'User created successfully',
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)

#         logger.error(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
