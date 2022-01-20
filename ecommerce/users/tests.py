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
            CustomUser, username="sharam",is_register=True , password="123" ,email="sharam@test.com" , phone="09108855")

    @tag('login_api_test')
    def test_login_api(self):
        customer2 = CustomUser.objects.create(username ="ali" , email="ali@test.com" , phone="1234" , password ='123' , is_register=True  )
        customer2.set_password('123')
        customer2.save()
        url = reverse('login_api')
        data_login = {
            "username": "ali",
            "password": "123"
        }
        response = self.client.post(url, data=data_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('register_api_test')
    def test_login(self):
        url = reverse('register_api')
        data=   {
                "username": "abolfazl123",
                "password": "123",
                "password2": "123",
                "email": "abolfazl@test.com",
                "phone": "123412542312",
                "city": "tehran"

            }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
