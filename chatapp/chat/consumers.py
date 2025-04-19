import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Channel, Membership


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_channel_name = self.scope['url_route']['kwargs']['channel_name']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.chat_channel_name}'

        if not await self.is_member(self.chat_channel_name):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Ensure room_group_name exists before trying to discard
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']
        print(f"Sending message: {message}")
        await self.send(text_data=json.dumps({'message': message}))

    async def is_member(self, channel_name):
        try:
            channel = await Channel.objects.aget(name=channel_name)
            return await Membership.objects.filter(user=self.user, channel=channel).aexists()
        except Channel.DoesNotExist:
            return False
