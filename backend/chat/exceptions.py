from rest_framework.exceptions import APIException
from rest_framework import status


class AuthenticationError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Kimlik doğrulama başarısız."
    default_code = "authentication_failed"


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Bu eylemi gerçekleştirme yetkiniz yok."
    default_code = "permission_denied"


class NotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Kaynak bulunamadı."
    default_code = "not_found"


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Geçersiz veri girdiniz."
    default_code = "validation_error"


class ConnectionError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Bağlantı hatası. Lütfen daha sonra tekrar deneyiniz."
    default_code = "connection_error"
