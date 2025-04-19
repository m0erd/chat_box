import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    logger.info(f"Channel '{serializer.instance.name}' created by user {request.user.username}.")
    raise ValidationError(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@error_handler
def join_channel(request, pk):
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        raise NotFoundError("Kanal bulunamadı.")

    membership, created = Membership.objects.get_or_create(user=request.user, channel=channel)
    # membership is just a placeholder for this case/membership'in amacı sadece mantığı kurmak,
    # eğer mevcut ise created pas geçilecek, yani false olacak

    logger.info(f"User {request.user.username} joined channel '{channel.name}'.")

    if created:
        return Response({"status": "joined"}, status=status.HTTP_201_CREATED)
    raise ValidationError("Zaten bu kanala üyesiniz.")


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
        raise NotFoundError("Kanal bulunamadı.")
    except Membership.DoesNotExist:
        logger.warning(f"User {request.user.username} tried to leave '{channel.name}' but is not a member.")
        raise ValidationError("Üye değilsiniz.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@error_handler
def my_channels(request):
    memberships = Membership.objects.filter(user=request.user)
    channels = [membership.channel for membership in memberships]
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
        raise NotFoundError("Kanal bulunamadı.")

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
        raise NotFoundError("Kanal veya mesaj bulunamadı.")

    if message.user != request.user:
        raise ValidationError("Sadece mesajın sahibi mesajı silebilir.")

    message.delete()
    return Response({"status": "message deleted"}, status=status.HTTP_204_NO_CONTENT)
