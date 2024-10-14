from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Task, User  # Use your custom User model
from .serializers import TaskSerializer, UserSerializer

# ViewSets for Users and Tasks
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)  # Filter tasks by the logged-in user
        status_filter = self.request.query_params.get('status', None)
        priority_filter = self.request.query_params.get('priority', None)
        due_date_filter = self.request.query_params.get('due_date', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if due_date_filter:
            queryset = queryset.filter(due_date=due_date_filter)

        return queryset

# Task Overview
@api_view(['GET'])
def taskOverview(request):
    tasks_urls = {
        'List': '/api/tasks/',
        'Detail View': '/api/tasks/<str:pk>/',
        'Create': '/api/tasks/create/',
        'Update': '/api/tasks/update/<str:pk>/',
        'Delete': '/api/tasks/delete/<str:pk>/',
        'Mark Complete': '/api/tasks/<str:pk>/mark-complete/',
        'Mark Incomplete': '/api/tasks/<str:pk>/mark-incomplete/',
    }
    return Response(tasks_urls)

# List all tasks (Function-Based View)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskList(request):
    tasks = Task.objects.filter(user=request.user)  # Only return tasks for the logged-in user
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# Retrieve task details (Function-Based View)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskDetail(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

# Create a task (Function-Based View)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Ensure task is assigned to the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a task (Function-Based View)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def taskUpdate(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a task (Function-Based View)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def taskDelete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return Response('Task deleted successfully', status=status.HTTP_204_NO_CONTENT)

# Custom Task Completion Handlers
def set_task_status(task, status):
    task.status = status
    task.completed_at = timezone.now() if status == 'Completed' else None
    task.save()
    return TaskSerializer(task).data

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_complete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if task.status == 'Completed':
        return Response({'error': 'Task is already marked as complete.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = set_task_status(task, 'Completed')
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_incomplete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if task.status == 'Pending':
        return Response({'error': 'Task is already marked as incomplete.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = set_task_status(task, 'Pending')
    return Response(data, status=status.HTTP_200_OK)

# User Management Views (if needed for custom actions)
@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def userUpdate(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user != user:
        return Response({'error': 'You are not allowed to update this user.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def userDelete(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user != user:
        return Response({'error': 'You are not allowed to delete this user.'}, status=status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response('User deleted successfully', status=status.HTTP_204_NO_CONTENT)
