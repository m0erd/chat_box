import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Channel, Membership


class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.chat_channel_name = self.scope['url_route']['kwargs']['channel_name']
    #     self.user = self.scope['user']
    #     # self.user = self.scope.get('user', None)
    #
    #     self.room_group_name = f'chat_{self.chat_channel_name}'
    #
    #     # if not await self.is_member(self.chat_channel_name):
    #     #     await self.close()
    #     #     return
    #
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #
    #     await self.accept()
    #     print("User in scope:", self.scope["user"])
    async def connect(self):
        self.user = self.scope['user']
        print("User in scope:", self.user)

        self.chat_channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.room_group_name = f'chat_{self.chat_channel_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     username = self.scope["user"]
    #     message = text_data_json.get('message')
    #     message = (str(username) + ": " + message)
    #     print(f"Received raw: {message}")
    #
    #     # user = self.scope["user"]
    #     # username = user.username if user.is_authenticated else "Anonymous"
    #
    #     if message:
    #         await self.channel_layer.group_send(
    #             self.room_group_name,
    #             {
    #                 'type': 'chat_message',
    #                 'message': message,
    #                 "username": str(self.scope["user"])
    #             }
    #         )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     username = self.scope["user"].username  # get sender username
    #
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message,
    #             'username': username,  # send username with message
    #         }
    #     )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    # async def chat_message(self, event):
    #     message = event['message']
    #     username = event["username"]
    #     print(f"Username: {username}")
    #     print(f"Sending message: {message}")
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         "username": username
    #     }))

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def is_member(self, channel_id):
        try:
            channel = await Channel.objects.aget(name=channel_id)
            return await Membership.objects.filter(user=self.user, channel=channel).aexists()
        except Channel.DoesNotExist:
            return False
