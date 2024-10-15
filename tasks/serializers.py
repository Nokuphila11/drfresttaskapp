from django.utils import timezone
from rest_framework import serializers
from .models import Task, User  # Import your custom User model

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # Include all fields; adjust as necessary

    # Custom validation to ensure the due date is in the future
    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    # Additional validation logic for task status and completed_at timestamp
    def validate(self, data):
        if data.get('status') == 'Completed' and not data.get('completed_at'):
            raise serializers.ValidationError("Completed tasks must have a completion timestamp (completed_at).")
        if data.get('status') != 'Completed' and data.get('completed_at'):
            raise serializers.ValidationError("Non-completed tasks should not have a completion timestamp (completed_at).")
        return data

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']  # Specify fields explicitly
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
            'profile_picture': {'required': False},  # Profile picture is optional
        }

    # Override create to hash password before saving the user
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    # Override update to handle password hashing correctly
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Hash the password if it's being updated
            validated_data.pop('password')

        return super().update(instance, validated_data)

    # Validate username to prevent duplicates
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    # Validate email to ensure uniqueness
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
