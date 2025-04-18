from rest_framework import serializers
from .models import Channel, Membership
from django.contrib.auth.models import User
from .models import Message


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'created_at', 'creator']


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'channel', 'joined_at']


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'channel', 'content', 'timestamp']
