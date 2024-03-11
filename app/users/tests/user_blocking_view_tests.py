import json
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from ..models.models import User
from ..views.views import UserBlockingView
import uuid


class UserBlockingViewTests(TestCase):
    """
    Tests for the UserBlockingView class
    """
    def setUp(self):
        self.view = UserBlockingView()
        self.user = User.objects.create(name='test_user')
        self.blocked_user = User.objects.create(name='blocked_user', nickname='blocked_user', email='blocked_user@email.com')
        self.blocked_user2 = User.objects.create(name='blocked_user2', nickname='blocked_user2', email="blocked_user2@email.com")
        self.blocked_user3 = User.objects.create(name='blocked_user3', nickname='blocked_user3', email="blocked_user3@email.com")
        self.user.blocked_users.add(self.blocked_user, self.blocked_user2)

    def test_get_blocked_users(self):
        url = reverse('user_blocks', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['blocked_users']), 2)

    def test_add_blocked_user(self):
        url = reverse('modify_blocks', args=[self.user.id, self.blocked_user3.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(self.user.blocked_users.count(), 3)

    def test_remove_blocked_user(self):
        url = reverse('modify_blocks', args=[self.user.id, self.blocked_user2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(self.user.blocked_users.count(), 1)

    def test_remove_blocked_user_nonexistent(self):
        url = reverse('modify_blocks', args=[self.user.id, self.blocked_user3.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(self.user.blocked_users.count(), 2)

    def test_get_blocked_users_nonexistent_user(self):
        url = reverse('user_blocks', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'User does not exist')

    def test_add_blocked_user_nonexistent_user(self):
        url = reverse('modify_blocks', args=[uuid.uuid4(), self.blocked_user3.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'User or blocked user does not exist')