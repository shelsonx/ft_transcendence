import json
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from ..models.models import User
from ..views.views import UserFriendshipView
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
