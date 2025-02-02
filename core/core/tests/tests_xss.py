from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your tests here.


class XSSVulnerabilityTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='amin', password='TESTPassword'
        )

    def test_xss_vulnerability(self):
        # 1. Create a potentially malicious input
        malicious_input = "<script>alert('XSS Attack!');</script>"  # Classic XSS payload

        # 2. Simulate a user submitting the malicious input (adjust as needed)
        data = {'message': malicious_input}  # 'message' is vulnerable field

        url = reverse('xss') 
        response = self.client.post(url, data)

        # 3. Assertions: Check for proper escaping/sanitization.
        # check it the malicious_input was escaped or not.

        # Check if the malicious input is present in the rendered HTML.
        self.assertNotContains(response, malicious_input) # Good - input is sanitized

        # Check if the *escaped* version of the input is present.
        escaped_input = "&lt;script&gt;alert('XSS Attack!');&lt;/script&gt;" # Expected escaped output
        self.assertNotContains(response, escaped_input)

    def test_xss_vulnerability_get(self): # Test for GET requests too
        # this test, tests malicious input in the url.
        malicious_input = "<script>alert('XSS Attack!');</script>"
        url = reverse('xss') + f'?message={malicious_input}' # Add malicious input as GET parameter
        response = self.client.get(url)
        escaped_input = "&lt;script&gt;alert('XSS Attack!');&lt;/script&gt;"
        self.assertNotContains(response, escaped_input)
