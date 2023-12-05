from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    chat_rooms = models.ManyToManyField('chat.ChatRoom', related_name='memberships_users')

    def __str__(self):
        return self.username
