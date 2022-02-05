from django.test import TestCase

# Create your tests here.


class SmokeTestCase(TestCase):
    def setup(self):
        self.value = 100

    def test_smoke(self):
        self.assertEqual(self.value, 100)