from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

@database_sync_to_async
def get_user(validated_token):
    try:
        return JWTAuthentication().get_user(validated_token)
    except:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract token from query string: ?token=xyz
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            scope["user"] = await get_user(validated_token)
        except Exception as e:
            print("JWT validation failed:", e)
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
