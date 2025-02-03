from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Comment

class IDORTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(
            username='testuser1', password='TESTPassword',
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2', password='TESTPassword',
        )

        self.comment1 = Comment.objects.create(user=self.user1, message="testcomment1")
        self.comment2 = Comment.objects.create(user=self.user2, message="testcomment2")

    def test_idor_vulnerability(self):
        """Tests for Insecure Direct Object References (IDOR)."""

        # Test access to another user's object
        self.client.force_login(self.user1)  # Log in as user1
        # Try to access comment2 (owned by user2)
        response = self.client.get(reverse('comment-detail', args=[self.comment2.id]))  

        # Check for appropriate status code (e.g., 403 Forbidden, 404 Not Found)
        self.assertIn(response.status_code, [403, 404])  # Or 401 if not logged in


    def test_accessing_objects_with_invalid_or_non_existent_IDs(self):
        self.client.force_login(self.user1)  # Log in as user1
        response = self.client.get(reverse('comment-detail', args=[1234]))
        self.assertEqual(response.status_code, 404)


    