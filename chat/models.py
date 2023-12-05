from django.db import models

class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    max_members = models.IntegerField()
    members = models.ManyToManyField('user.User', related_name='chat_rooms_users')

    def __str__(self):
        return self.name

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')  # Adjust upload_to as needed
    # Add more fields as required

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey('user.User', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.ForeignKey(Attachment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} - {self.text[:20]}"
