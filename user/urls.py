from django.urls import path
from .views import join_chat_room, leave_chat_room, create_user, delete_users, get_user

urlpatterns = [
    path('user/join/', join_chat_room, name='join-chat-room'),
    path('users/leave/', leave_chat_room, name='leave-chat-room'),
    path('users/create/', create_user, name='create-user'),
    path('users/delete/', delete_users, name='delete-users'),
    path('users/delete/<int:user_id>/', delete_users, name='delete-user-by-id'),
    path('users/', get_user, name='get-users'),
    path('users/<int:user_id>/', get_user, name='get-user-by-id'),
]