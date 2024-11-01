from django.urls import path
from .consumer import MessageConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', MessageConsumer.as_asgi()),
]
