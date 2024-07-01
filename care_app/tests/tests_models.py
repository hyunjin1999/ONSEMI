from django.test import TestCase
from auth_app.models import User
from care_app.models import Senior, Care
from django.shortcuts import get_object_or_404

# Create your tests here.


class TestModels(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="mmnmn",
            email="adgfdg@mail.com",
            user_type="FAMILY",
            password="qwer",
            phone_number="101-1010-1010",
        )

        senior = Senior(
            address="aa",
            name="aa",
            age=10,
            gender="MALE",
            phone_number="010-0101-0101",
            user_id=user,
        )
        senior.save()

        care = Care(care_type="VISIT", user_id=user)
        care.save()
        care.seniors.add(senior)

    def testSeniorModel(self):
        senior_list = Senior.objects.filter(user_id=User.objects.get(username="mmnmn"))
        self.assertEqual(len(senior_list), 1)

    def testCareModel(self):
        care_list = Care.objects.filter(user_id=User.objects.get(username="mmnmn"))
        senior_list = Senior.objects.filter(user_id=User.objects.get(username="mmnmn"))

        self.assertEqual(len(care_list), 1)
