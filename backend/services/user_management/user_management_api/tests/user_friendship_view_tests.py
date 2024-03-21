import json
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from user_management_api.models.models import User
from user_management_api.views.user_friendship import UserFriendshipView
import uuid

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
        self.new_user = User.objects.create(name='new_user', nickname='new_user', email='new_user@email.com', avatar='new_user.jpg')
        self.new_user2 = User.objects.create(name='new_user2', nickname='new_user2', email='new_user2@email.com', avatar='new_user2.jpg')
        self.valid_uuid = uuid.uuid4()

    def test_add_new_friend(self):
        user_id = str(self.new_user.id)
        friend_id = str(self.new_user2.id)
        request = self.factory.post('/users/' + user_id + '/friends', {'friend_id': friend_id})
        response = self.view.post(request, user_id, friend_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend added successfully', 'status_code': 200})
        self.assertEqual(self.new_user.friends.count(), 1)
        self.assertEqual(self.new_user.friends.first(), self.new_user2)

    def test_get_friends(self):
        user_id = str(self.user1.id)
        request = self.factory.get('/users/' + user_id + '/friends')
        response = self.view.get(request, user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'friends': [], 'status_code': 200})

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
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend added successfully', 'status_code': 200})
        self.assertEqual(self.user1.friends.count(), 1)
        self.assertEqual(self.user1.friends.first(), self.user2)

    def test_add_existing_friend(self):
        url = reverse('modify_friends', args=[self.new_user.id, self.new_user2.id])
        response = self.client.post(url)
        new_url = reverse('modify_friends', args=[self.new_user.id, self.new_user2.id])
        response2 = self.client.post(new_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 400)
        data = json.loads(response2.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Friendship already exists')

    def test_remove_friend(self):
        self.user1.friends.add(self.user2)
        user_id = str(self.user1.id)
        friend_id = str(self.user2.id)
        request = self.factory.delete('/users/' + user_id + '/friends', {'friend_id': friend_id})
        response = self.view.delete(request, user_id, friend_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend removed successfully', 'status_code': 200})
        self.assertEqual(self.user1.friends.count(), 0)

    def test_remove_nonexistent_friend(self):
        user_id = str(self.user1.id)
        friend_id = str(self.user2.id)
        request = self.factory.delete('/users/' + user_id + '/friends', {'friend_id': friend_id})
        response = self.view.delete(request, user_id, friend_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success', 'message': 'Friend removed successfully', 'status_code': 200})
        self.assertEqual(self.user1.friends.count(), 0)
