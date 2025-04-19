import os
import jwt
from urllib.parse import parse_qs

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


SECRET_KEY = os.getenv('SECRET_KEY')


@database_sync_to_async
def get_user(user_id):
    try:
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if token is None:
            scope["user"] = AnonymousUser()
        else:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user = await get_user(payload.get("user_id"))
                scope["user"] = user or AnonymousUser()
            except (ExpiredSignatureError, InvalidTokenError):
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
