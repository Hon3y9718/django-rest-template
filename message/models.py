from django.db import models
from django.contrib import admin
from user.models import User

# Create your models here.

class Room(models.Model):
    room = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sender')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    isFile = models.BooleanField(default=False)
    isFromSystem = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.room.room}"
    
class MessageAdmin(admin.ModelAdmin):
    search_fields = ["id", "room", "sender", "message", "timestamp", "read", "isFile", "isFromSystem"]