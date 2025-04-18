from rest_framework import serializers
from .models import Channel, Membership
from django.contrib.auth.models import User


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'created_at', 'creator']


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'channel', 'joined_at']
