import logging

from django.db.models import Q
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Channel, Membership, Message
from .serializers import ChannelSerializer, MessageSerializer
from .exceptions import NotFoundError, ValidationError
from core.utils import error_handler


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@error_handler
def create_channel(request):
    serializer = ChannelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        logger.info(f"Channel '{serializer.instance.name}' created by user {request.user.username}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.warning(f"Channel creation failed by user {request.user.username}. Errors: {serializer.errors}")
    raise ValidationError(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@error_handler
def join_channel(request, pk):
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        raise NotFoundError("Channel not found.")

    membership, created = Membership.objects.get_or_create(user=request.user, channel=channel)

    logger.info(f"User {request.user.username} joined channel '{channel.name}'.")

    if created:
        return Response({"status": "joined"}, status=status.HTTP_201_CREATED)
    raise ValidationError("You are already member of this channel.")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@error_handler
def leave_channel(request, pk):
    try:
        channel = Channel.objects.get(pk=pk)
        membership = Membership.objects.get(user=request.user, channel=channel)
        membership.delete()

        logger.info(f"User {request.user.username} left channel '{channel.name}'.")
        return Response({"status": "left"}, status=status.HTTP_204_NO_CONTENT)
    except Channel.DoesNotExist:
        raise NotFoundError("Channel not found.")
    except Membership.DoesNotExist:
        logger.warning(f"User {request.user.username} tried to leave '{channel.name}' but is not a member.")
        raise ValidationError("You are not member of the channel.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@error_handler
def my_channels(request):
    # memberships = Membership.objects.filter(user=request.user)
    # channels = [membership.channel for membership in memberships]
    # serializer = ChannelSerializer(channels, many=True)
    # return Response(serializer.data)

    user = request.user
    memberships = Membership.objects.filter(user=user).values_list('channel_id', flat=True)
    channels = Channel.objects.filter(Q(id__in=memberships) | Q(creator=user)).distinct()
    # Q(id__in=memberships): This checks for channels where the user is a member (by Membership model)
    # Q(creator=user): This checks for channels where the user is the creator.

    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@error_handler
def list_messages(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({"detail": "Channel not found."}, status=status.HTTP_404_NOT_FOUND)

    messages = Message.objects.filter(channel=channel)
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@error_handler
def send_message(request, channel_id):
    try:
        channel = Channel.objects.get(pk=channel_id)
    except Channel.DoesNotExist:
        raise NotFoundError("Channel not found.")

    message = Message.objects.create(
        user=request.user,
        channel=channel,
        content=request.data.get("content")
    )
    return Response({"status": "message sent"}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@error_handler
def delete_message(request, channel_id, message_id):
    try:
        channel = Channel.objects.get(pk=channel_id)
        message = Message.objects.get(id=message_id, channel=channel)
    except (Channel.DoesNotExist, Message.DoesNotExist):
        raise NotFoundError("Channel or message not found.")

    if message.user != request.user:
        raise ValidationError("Message can be delete by only the owner of the message.")

    message.delete()
    return Response({"status": "message deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@error_handler
def list_channels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@error_handler
def channel_name(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
        return Response({"channel_name": channel.name})
    except Channel.DoesNotExist:
        return Response({"error": "Channel not found"}, status=404)



@never_cache
def test_socket_view(request):
    return render(request, 'chat/test_socket.html')

def index(request):
    return render(request, 'base.html')

class FrontendAppView(TemplateView):
    template_name = 'chat/chat.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
