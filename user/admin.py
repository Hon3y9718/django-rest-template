from django.contrib import admin

from user.models import User, UserAdmin, UserRole

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserRole)