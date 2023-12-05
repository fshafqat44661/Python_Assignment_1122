from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import ChatRoom
from .serializers import UserSerializer
from .models import User


@api_view(['POST'])
def join_chat_room(request):
    user_id = request.data.get('id')
    room_id = request.data.get('room_id')

    try:
        user = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=room_id)

        # Check if the user is already a member of the chat room
        if user in chat_room.members.all():
            return Response({'message': 'User is already in the chat room'}, status=status.HTTP_400_BAD_REQUEST)

        if chat_room.members.count() >= chat_room.max_members:
            return Response({'message': 'Chat room is full. Cannot join at the moment.'}, status=status.HTTP_400_BAD_REQUEST)

        chat_room.members.add(user)

        # Update the members list in the chat room to include the user ID
        chat_room_members = chat_room.members.values_list('id', flat=True)
        if user_id not in chat_room_members:
            chat_room_members = list(chat_room_members)
            chat_room_members.append(user_id)
            chat_room.members.set(chat_room_members)

        return Response({'message': f'User with ID {user_id} joined chat room {chat_room.name}'},
                        status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def leave_chat_room(request):
    user_id = request.data.get('id')
    room_id = request.data.get('room_id')

    try:
        user = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=room_id)

        # Check if the user is a member of the chat room
        if user not in chat_room.members.all():
            return Response({'message': 'User is not in the chat room'}, status=status.HTTP_400_BAD_REQUEST)

        chat_room.members.remove(user)

        # Update the members list in the chat room to remove the user ID
        chat_room_members = chat_room.members.values_list('id', flat=True)
        if user_id in chat_room_members:
            chat_room_members = list(chat_room_members)
            chat_room_members.remove(user_id)
            chat_room.members.set(chat_room_members)

        return Response({'message': f'User with ID {user_id} left chat room {chat_room.name}'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room does not exist'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def create_user(request):
    data = request.data

    if isinstance(data, list):
        serializer = UserSerializer(data=data, many=True)
    else:  # If it's not a list, create a single user
        serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_users(request, user_id=None):
    if user_id is None:  # If no ID provided, delete all users
        User.objects.all().delete()
        return Response({'message': 'All users deleted successfully!'})
    else:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'message': f'User with ID {user_id} deleted successfully!'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

@api_view(['GET'])
def get_user(request, user_id=None):
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)
    else:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)