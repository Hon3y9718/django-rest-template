from django.urls import path
from . import views

urlpatterns = [
    # Room URLs
    path('rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', views.RoomRetrieveUpdateDestroyView.as_view(), name='room-detail'),

    # Message URLs
    path('rooms/<int:room_id>/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
]
