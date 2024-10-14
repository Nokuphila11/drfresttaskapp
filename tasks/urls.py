from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define the router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Task-related URLs using function-based views
    path('overview/', views.taskOverview, name='task-overview'),
    path('tasks/', views.taskList, name='task-list'),
    path('tasks/<str:pk>/', views.taskDetail, name='task-detail'),
    path('tasks/create/', views.taskCreate, name='task-create'),
    path('tasks/update/<str:pk>/', views.taskUpdate, name='task-update'),
    path('tasks/delete/<str:pk>/', views.taskDelete, name='task-delete'),

    # User-related URLs (function-based views)
    path('users/create/', views.userCreate, name='user-create'),
    path('users/update/<str:pk>/', views.userUpdate, name='user-update'),
    path('users/delete/<str:pk>/', views.userDelete, name='user-delete'),

    # New endpoints for marking tasks complete/incomplete
    path('tasks/<str:pk>/mark-complete/', views.mark_task_complete, name='mark-task-complete'),
    path('tasks/<str:pk>/mark-incomplete/', views.mark_task_incomplete, name='mark-task-incomplete'),

    # Token authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
