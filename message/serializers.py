from rest_framework import serializers
import django_filters
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'read', 'message', 'timestamp', 'isFile', 'isFromSystem', 'created_at', 'updated_at']

class MessageFilters(django_filters.FilterSet):
    message = django_filters.CharFilter(field_name='message', lookup_expr='icontains')
    
    class Meta:
       model = Message
       fields = ['id', 'room', 'sender', 'read', 'message', 'timestamp', 'isFile', 'isFromSystem']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room', 'created_at', 'updated_at']
