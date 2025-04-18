import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import Channel, Membership
from .serializers import ChannelSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = self.scope['url_route']['kwargs']['channel_name']
        self.user = self.scope['user']

        if not await self.is_member(self.channel_name):
            await self.close()
            return

        self.room_group_name = f'chat_{self.channel_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def is_member(self, channel_name):
        try:
            channel = Channel.objects.get(name=channel_name)
            return Membership.objects.filter(user=self.user, channel=channel).exists()
        except Channel.DoesNotExist:
            return False
