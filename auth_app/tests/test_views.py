from django.test import TestCase
from auth_app.models import User

# Create your tests here.


class AuthViewTest(TestCase):

    def test_login_view_status_code(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)
