from django.test import TestCase
from django.db import connection, IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Comment


class SQLInjectionTests(TestCase):

    def setUp(self):
        # Create a user for testing (important for models with ForeignKey to User)
        self.user1 = get_user_model().objects.create_user(
            username='amin', password='TESTPassword'
        )
        self.user2 = get_user_model().objects.create_user(
            username='jamali', password='TESTPassword'
        )

        # Create some test comments (replace with your data)
        commnet1 = Comment.objects.create(message="let's test sql injection", user=self.user1)
        comment2 = Comment.objects.create(message="does the tests pass?", user=self.user2)
        self.commnets = [commnet1, comment2]


    def test_sql_injection_get_view(self):
        # Simulate a vulnerable input get method.
        malicious_input = " 'OR '1'='1 ---' "
        query = f"SELECT * FROM core_comment WHERE message = '{malicious_input}'"
        Comment.objects.raw(query)
        url = reverse('sqlinjection') + f'?message={malicious_input}'
        response = self.client.get(url)
        # we expect the query to return nothing (because the input is malicious but handled),
        # and the result is empty queryset.
        for comment in self.commnets:
            self.assertNotContains(response, comment)


    def test_sql_injection_post_get_view(self):
        # Simulate a vulnerable input, post method.
        malicious_input = " 'OR '1'='1 ---' "
        query = f"SELECT * FROM core_comment WHERE message = '{malicious_input}'"
        data = {'message':query}
        url = reverse('sqlinjection')
        response1 = self.client.post(url, data)
        # we expect the query to return nothing (because the input is malicious but handled),
        # and the result is empty queryset.
        response2 = self.client.get(url)

        for comment in self.commnets:
            self.assertNotContains(response2, comment)


    def test_sql_injection_orm_filter_exact(self):
        malicious_input = " 'OR '1'='1 ---' "
        results = Comment.objects.filter(message=malicious_input)
        self.assertEqual(len(results), 0)
