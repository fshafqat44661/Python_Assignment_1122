from django.urls import path
from .views import ChatRoomCreate, MessageListCreate, ChatRoomList, DeleteAllChatRooms
from django.conf.urls import include

urlpatterns = [
    path('chatrooms/', ChatRoomCreate.as_view(), name='chatroom-list-create'),
    path('messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('chatrooms/list/', ChatRoomList.as_view(), name='chatroom-list'),
    path('chatrooms/delete-all/', DeleteAllChatRooms.as_view(), name='delete-all-chatrooms'),

]
