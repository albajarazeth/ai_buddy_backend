from django.db import models
from django.contrib.auth.models import User   # use Django's built-in user


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} for {self.user.username}"

class Message(models.Model):
    SENDER_CHOICES = [
        ('USER', 'User'),
        ('AI', 'AI'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")

    sender = models.CharField(max_length=4, choices=SENDER_CHOICES, default='USER')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} message in session {self.session.id}"
