from django.shortcuts import render

# Create your views here.
# yourapp/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer

# Room CRUD Views
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# Message CRUD Views
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Filter messages by room ID if provided in the URL
        room_id = self.kwargs.get('room_id')
        if room_id:
            return Message.objects.filter(room_id=room_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
