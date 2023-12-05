from rest_framework import serializers
from .models import ChatRoom, Message, Attachment

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer()  # Include attachment details

    class Meta:
        model = Message
        fields = '__all__'
