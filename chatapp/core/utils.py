from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


def error_handler(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except APIException as e:
            return Response(
                {"error": str(e.detail)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {"error": "Beklenmedik bir şeyler ters gitti, lütfen tekrar deneyin(500)."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return _wrapped_view
