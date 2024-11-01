import django_filters
from rest_framework import serializers
from user.models import User, UserRole

##### User Role #####
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'role']

class RoleFilters(django_filters.FilterSet):
    role = django_filters.CharFilter(field_name='role', lookup_expr='icontains')
    
    class Meta:
       model = UserRole
       fields = ['id', 'role']

##### User #####
class UserSerializer(serializers.ModelSerializer):
    # For registration: use PrimaryKeyRelatedField to handle the role as an ID
    role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(), write_only=True)
    
    # For fetching the user: get role_name when reading the user data
    role_name = serializers.CharField(source='role.role', read_only=True)
    role_id = serializers.IntegerField(source='role.id', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'notification_token', 'is_active', 'is_verified', 'avatar', 'role', 'role_id', 'role_name', 'updated_at', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class BasicUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'created_at', 'updated_at']

class UserFilters(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'notification_token', 'is_active', 'is_verified', 'avatar', 'updated_at', 'created_at']

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
