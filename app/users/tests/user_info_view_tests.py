import json
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from ..models.models import User
from ..views.views import UserInfoView
import uuid

class UserInfoViewTests(TestCase):
    """
    Tests for the UserInfoView class
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.view = UserInfoView()
        self.user = User.objects.create(name='testuser', email='user@example.com')
        self.valid_uuid = self.user.id  # Assuming id is a UUID field
        self.nonexistent_uuid = uuid.uuid4()  # Valid format but doesn't exist in the database

    def test_get_user_valid_uuid(self):
        # Test retrieving an existing user by valid UUID
        response = self.client.get(reverse('user_detail', args=[str(self.valid_uuid)]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.content.decode())

    def test_get_user_nonexistent_uuid(self):
        # Test retrieving a non-existent user by valid UUID
        response = self.client.get(reverse('user_detail', args=[str(self.nonexistent_uuid)]))
        self.assertEqual(response.status_code, 404)

    def test_delete_user_valid_uuid(self):
        response = self.client.delete(reverse('user_detail', args=[str(self.valid_uuid)]))
        self.assertEqual(response.status_code, 200)
        # Verify the user was deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.valid_uuid)

    def test_delete_user_nonexistent_uuid(self):
        response = self.client.delete(reverse('user_detail', args=[str(self.nonexistent_uuid)]))
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        response = self.client.get(reverse('user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.content.decode())

    def test_delete_existing_user(self):
        user_id = str(self.valid_uuid)
        request = self.factory.delete('/users/' + user_id)
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'User deleted successfully', 'status_code': 200})

    def test_delete_non_existing_user(self):
        user_id = str(self.nonexistent_uuid)
        request = self.factory.delete('/users/' + user_id)
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'User does not exist', 'status_code': 404})

    def test_delete_invalid_user_id(self):
        user_id = 'abc'
        request = self.factory.delete('/users/' + user_id)
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'Invalid UUID', 'status_code': 400})
