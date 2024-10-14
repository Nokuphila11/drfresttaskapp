from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Task

class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('user-create')

    def test_create_user(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # 1 existing user + new user

    def test_user_creation_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AuthTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token_url = reverse('token_obtain_pair')

    def test_obtain_token(self):
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class TaskTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.task_url = reverse('task-create')
        self.client.login(username='testuser', password='testpassword123')

    def test_create_task(self):
        task_data = {
            'title': 'Test Task',
            'description': 'Task description',
            'due_date': '2024-12-31',
            'priority': 'High',
            'status': 'Pending',
            'user': self.user.id
        }
        response = self.client.post(self.task_url, task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_creation_without_authentication(self):
        self.client.logout()  # Log out the user
        task_data = {
            'title': 'Test Task',
            'description': 'Task description',
            'due_date': '2024-12-31',
            'priority': 'High',
            'status': 'Pending',
            'user': self.user.id
        }
        response = self.client.post(self.task_url, task_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tasks(self):
        # Create a task for the authenticated user
        Task.objects.create(
            title='Another Test Task',
            description='Another description',
            due_date='2024-12-31',
            priority='Medium',
            status='Pending',
            user=self.user
        )
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 task

