from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet, RegisterView, ProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView, LogoutView

# Define the router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Include the router URLs for User and Task ViewSets (this handles standard CRUD operations)
    path('api/', include(router.urls)),

    # Custom task-related URLs using function-based views
    path('tasks/', views.taskList, name='task-list'),
    path('tasks/create/', views.taskCreate, name='task-create'),  # Create should be before <str:pk> to avoid conflicts
    path('tasks/<int:pk>/', views.taskDetail, name='task-detail'),  # Expecting an integer pk
    path('tasks/update/<int:pk>/', views.taskUpdate, name='task-update'),
    path('tasks/delete/<int:pk>/', views.taskDelete, name='task-delete'),
    path('tasks/<int:pk>/mark-complete/', views.mark_task_complete, name='mark-task-complete'),
    path('tasks/<int:pk>/mark-incomplete/', views.mark_task_incomplete, name='mark-task-incomplete'),

    # New endpoints for marking tasks complete/incomplete
    path('tasks/<int:pk>/mark-complete/', views.mark_task_complete, name='mark-task-complete'),
    path('tasks/<int:pk>/mark-incomplete/', views.mark_task_incomplete, name='mark-task-incomplete'),

    # Token authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User authentication URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]
