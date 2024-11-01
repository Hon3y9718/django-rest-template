from django.contrib import admin
from .models import Message, MessageAdmin, Room

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Room)