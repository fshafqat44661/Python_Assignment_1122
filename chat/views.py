from rest_framework import generics
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChatRoomList(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class DeleteAllChatRooms(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        ChatRoom.objects.all().delete()
        return Response("All chat rooms deleted successfully", status=status.HTTP_204_NO_CONTENT)
class ChatRoomCreate(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            members_ids = request.data.get('members', [])
            existing_user_ids = set()

            # Create the chat room first
            chat_room = ChatRoom.objects.create(
                name=serializer.validated_data['name'],
                max_members=serializer.validated_data['max_members']
            )

            for member_id in members_ids:
                if member_id in existing_user_ids:
                    print(f"Duplicate user ID: {member_id}. Skipping duplicate user.")
                    continue
                existing_user_ids.add(member_id)

                # Check if the user exists
                user = get_object_or_404(User, id=member_id)

                # Add the user to the chat room
                chat_room.members.add(user)

                # Update the user's chat_rooms field with the chat room ID
                user.chat_rooms.add(chat_room.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save message with sender and attachment
            sender = request.user
            attachment = request.FILES.get('attachment')  # Assuming attachment is sent via form-data
            serializer.save(sender=sender, attachment=attachment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


channel_layer = get_channel_layer()


def send_message_to_chat_room(room_id, sender_id, message_text):
    room_group_name = f'chat_{room_id}'

    sender = User.objects.get(id=sender_id)
    chat_room = ChatRoom.objects.get(id=room_id)

    # Create and save the message
    message = Message.objects.create(
        text=message_text,
        sender=sender,
        chat_room=chat_room
        # Include other relevant fields as needed
    )

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'message': message.text,
            'sender_id': sender_id,
            'room_id': room_id
        }
    )