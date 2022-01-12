from django.test import TestCase
from rest_framework.test import APITestCase
from model_mommy import mommy
from .models import CustomUser
from django.test import tag
from django.urls import reverse
from rest_framework import status


# Create your tests here.

class TestUnit(APITestCase):
    def setUp(self):
        self.customer1 = mommy.make(
            CustomUser, user_type="CT", username="sharam", password="123")

    @tag('login_api')
    def test_login_api(self):
        url = reverse('users:login_suplier')
        data = {
            "username": "sharam",
            "password": "123"
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('register_api')
    def test_login(self):
        url = reverse('users:register_api')
        data=   {
                "username": "abolfazl123",
                "password": "123",
                "password2": "123",
                "email": "abolfazl@test.com",
                "phone": "123412542312",
                "city": "tehran"

            }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
