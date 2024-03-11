import json
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from .models.models import User
from .views.views import UserInfoView, UserFriendshipView, UserBlockingView
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
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'User deleted successfully'})

    def test_delete_non_existing_user(self):
        user_id = str(self.nonexistent_uuid)
        request = self.factory.delete('/users/' + user_id)
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'User does not exist'})

    def test_delete_invalid_user_id(self):
        user_id = 'abc'
        request = self.factory.delete('/users/' + user_id)
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'Invalid user id'})

class UserFriendshipViewTests(TestCase):
    """
    Tests for the UserFriendshipView class
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.view = UserFriendshipView()
        self.user1 = User.objects.create(name='user1', nickname='user1', email='user1@email.com', avatar='user1.jpg')
        self.user2 = User.objects.create(name='user2', nickname='user2', email='user2@email.com', avatar='user2.jpg')
        self.user3 = User.objects.create(name='user3', nickname='user3', email='user3@email.com', avatar='user3.jpg')
        self.valid_uuid = uuid.uuid4()

    def test_get_friends(self):
        user_id = str(self.user1.id)
        request = self.factory.get('/users/' + user_id + '/friends')
        response = self.view.get(request, user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'friends': []})

        self.user1.friends.add(self.user2)
        self.user1.friends.add(self.user3)

        response = self.view.get(request, user_id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user2')
        self.assertContains(response, 'user3')
        self.assertNotContains(response, 'user1')
        self.assertNotContains(response, 'user4')

    def test_add_friend(self):
        user_id = str(self.user1.id)
        friend_id = str(self.user2.id)
        request = self.factory.post('/users/' + user_id + '/friends', {'friend_id': friend_id})
        response = self.view.post(request, user_id, friend_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend added successfully'})
        self.assertEqual(self.user1.friends.count(), 1)
        self.assertEqual(self.user1.friends.first(), self.user2)

    def test_add_friend_missing_parameter(self):
        user_id = str(self.user1.id)
        request = self.factory.post('/users/' + user_id + '/friends')
        response = self.view.post(request, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'Missing parameter: friend_id'})
        self.assertEqual(self.user1.friends.count(), 0)

    def test_remove_friend(self):
        self.user1.friends.add(self.user2)
        user_id = str(self.user1.id)
        friend_id = str(self.user2.id)
        request = self.factory.delete('/users/' + user_id + '/friends', {'friend_id': friend_id})
        response = self.view.delete(request, user_id, friend_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend removed successfully'})
        self.assertEqual(self.user1.friends.count(), 0)

    def test_remove_friend_missing_parameter(self):
        self.user1.friends.add(self.user2)
        user_id = str(self.user1.id)
        request = self.factory.delete('/users/' + user_id + '/friends')
        response = self.view.delete(request, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': 'Missing parameter: friend_id'})
        self.assertEqual(self.user1.friends.count(), 1)

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