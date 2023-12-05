from rest_framework import serializers
from .models import User
from chat.models import ChatRoom

class UserSerializer(serializers.ModelSerializer):
    chat_rooms = serializers.PrimaryKeyRelatedField(
        queryset=ChatRoom.objects.all(),
        required=False,  # Set the field as optional
        many=True
    )

    class Meta:
        model = User
        fields = ['id','username', 'phone_number', 'chat_rooms']  # Include the chat_rooms field

    def create(self, validated_data):
        chat_rooms = validated_data.pop('chat_rooms', [])  # Get the chat_rooms or default to empty list
        user = User.objects.create(**validated_data)
        user.chat_rooms.add(*chat_rooms)
        return user
