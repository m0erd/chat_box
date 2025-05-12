from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<channel_name>\w+)/$', consumers.ChatConsumer.as_asgi()),  # \w+, matches alphanumeric characters and underscores only
    # re_path(r"ws/chat/(?P<channel_name>[\w-]+)/$", consumers.ChatConsumer.as_asgi()),  # [\w-]+ this includes hyphens either
    re_path(r'ws/chat/(?P<channel_id>\d+)/$', consumers.ChatConsumer.as_asgi()),

]
