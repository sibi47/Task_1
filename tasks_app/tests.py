from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.urls import reverse

User = get_user_model()

class TaskAPITest(APITestCase):

    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        self.admin = User.objects.create_user(username="admin1", password="adminpass", is_staff=True)

        # Tasks
        self.task1 = Task.objects.create(
            title="Task 1",
            description="Task for user1",
            assigned_to=self.user1,
            status="Pending"
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="Task for user2",
            assigned_to=self.user2,
            status="Pending"
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_user_can_only_see_their_tasks(self):
        self.authenticate(self.user1)
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see their own task
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task 1')

    def test_user_cannot_access_others_task(self):
        self.authenticate(self.user1)
        url = reverse('tasks-detail', args=[self.task2.id])
        response = self.client.get(url)
        # Should be forbidden or 404 depending on your view
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_user_can_complete_own_task(self):
        self.authenticate(self.user1)
        url = reverse('tasks-detail', args=[self.task1.id])
        response = self.client.put(url, {
            'status': 'Completed',
            'completion_report': 'Done successfully',
            'worked_hours': 5
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'Completed')
        self.assertEqual(self.task1.worked_hours, 5)

    def test_admin_can_view_any_task_report(self):
        self.task2.status = 'Completed'
        self.task2.completion_report = 'Admin report view'
        self.task2.worked_hours = 4
        self.task2.save()

        self.authenticate(self.admin)
        url = reverse('task-report', args=[self.task2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completion_report'], 'Admin report view')
