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
        self.customer1 = mommy.make(CustomUser, username="sharam", is_register=True,
                                    password="123", email="sharam@test.com", phone="09108858899")

    @tag('login_api_test')
    def test_login_api(self):
        customer2 = CustomUser.objects.create(
            username="ali", email="ali@test.com", phone="1234", password='123', is_register=True)
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
        data = {
            "username": "farid2",
            "password": "123",
            "password2": "123",
            "email": "farid2@test.com",
            "phone": "09334029971",
            "city": "tehran"

        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag("generate_otp_test")
    def test_generate_otp(self):
        url = reverse('generate_otp_login')
        data = {"phone": self.customer1.phone}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('test_acitvate_phone')
    def test_activate_phone(self):
        url = reverse('register_api')
        data = {
            "username": "reza",
            "password": "123",
            "password2": "123",
            "email": "reza@test.com",
            "phone": "09334029971",
            "city": "tehran"

        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_activate = reverse('activate_user')
        data_activate={
            "phone":"09334029971",
            "otp":response.data["otp"]
        }
        response_activate = self.client.post(url_activate, data=data_activate)
        self.assertEqual(response_activate.status_code, status.HTTP_202_ACCEPTED)

    @tag('test_login_phone')
    def test_login_phone(self):
        customer2 = CustomUser.objects.create(
            username="ali", email="ali@test.com", phone="09334029971", password='123', is_register=True)
        customer2.set_password('123')
        customer2.save()

        
        url = reverse('generate_otp_login')
        data = {"phone": customer2.phone}
        response_otp = self.client.post(url, data=data)
        self.assertEqual(response_otp.status_code, status.HTTP_201_CREATED)
        url = reverse('login_api')
        data_login = {
            "phone": "09334029971",
            "otp": response_otp.data["otp"]
        }        
        response = self.client.post(url, data=data_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
