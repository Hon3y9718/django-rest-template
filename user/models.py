from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# Create your models here.
class UserRole(models.Model):
    role = models.CharField(max_length=255) ## Recruiter, Candidate, Admin, Super Admin
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role + " : " + str(self.id)

class User(AbstractUser):
    last_name = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=500)
    username = models.CharField(max_length=255, unique=True)
    avatar = models.CharField(max_length=500, default="https://cdn-icons-png.flaticon.com/512/149/149071.png", null=True, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name="role_name", default=1)
    notification_token = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email + " " + str(self.id)
    
class UserAdmin(admin.ModelAdmin):
    search_fields = ["id", "first_name", "last_name", "email", "username"]


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    is_deleted = models.BooleanField(default=False)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
