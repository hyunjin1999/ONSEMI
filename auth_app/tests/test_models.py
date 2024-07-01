from django.test import TestCase
from auth_app.models import User

# Create your tests here.


class AuthModelTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username="test0000",
            password="qwerqwer",
            phone_number="010-1234-5678",
            email="test0000@mail.com",
            user_type="FAMILY",
        )

        User.objects.create_superuser(
            username="admin0000",
            password="qwerqwer",
            email="test0001@mail.com",
            user_type="ADMIN",
        )

    def test_user(self):
        user = User.objects.get(username="test0000")

        self.assertEqual(user.email, "test0000@mail.com")

    def test_superuser(self):
        user = User.objects.get(username="admin0000")

        self.assertEqual(user.user_type, "ADMIN")
