from django.test import TestCase
from django.urls import reverse

class HelloWorldTest(TestCase):
    def test_hello_world(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, World!")