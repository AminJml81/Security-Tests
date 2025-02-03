from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

from datetime import timedelta


class SessionManagementTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(
            username='testuser1', password='TESTPassword',
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2', password='TESTPassword',
        )
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'
        settings.SESSION_COOKIE_AGE = 2  # Set a short session lifetime for testing.
        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False # it is not browser close.


    def test_session_creation_on_login(self):
        """Tests that a session is created upon successful login."""
        self.client.post(reverse('login'), {'username': 'testuser1', 'password': 'TESTPassword'})
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user1.id))


    def test_session_expiry(self):
        """Tests session expiry (you'll likely need to configure settings.SESSION_COOKIE_AGE)."""
        #  NOTE: Django's test client by default uses a cookie storage that clears the session after each request.
        #  To properly test session expiry, you'll need to use a persistent session store (like the database or cache).
        #  This example uses the database session store.
        #  'django.contrib.sessions' must be in the INSTALLED_APPS.

        self.client.post(reverse('login'), {'username': 'testuser1', 'password': 'TESTPassword'})
        session_id = self.client.cookies['sessionid'].value
        
        # getting session from the database.
        session = Session.objects.get(session_key=session_id)

        # Simulate some time passing (in a real app, SESSION_COOKIE_AGE handles this automatically)
        session.expire_date = timezone.now() - timedelta(seconds=settings.SESSION_COOKIE_AGE + 1) # 1 second to ensure expiry
        session.save()

        # make request to protected view.
        response = self.client.get(reverse('protected'))

        self.assertRedirects(response, reverse('login')) # Check redirect to login
        self.assertNotIn('_auth_user_id', self.client.session)  # Double check that the auth is not in the session


    def test_session_deletion_on_logout(self):
        """Tests that the session is deleted upon logout."""
        self.client.login(username='testuser', password='testpassword')
        self.client.get(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
