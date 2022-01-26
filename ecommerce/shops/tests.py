from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from django.test import tag
from django.urls import reverse
from rest_framework import status

from products.models import Product
from users.models import CustomUser
from .models import Shop


# Create your tests here.
class TestUnit(APITestCase):
    def setUp(self):
        self.suplier1 = mommy.make(
            CustomUser, user_type="SL", username="farid")
        self.customer1 = mommy.make(
            CustomUser, user_type="CT", username="sharam")
        self.shop1 = mommy.make(Shop, shop_type="SUP",
                                author=self.customer1, is_active=True)
        self.shop2 = mommy.make(Shop, shop_type="HYP", author=self.customer1)
        self.product1 = mommy.make(Product, shop=self.shop1)
        self.product2 = mommy.make(Product, shop=self.shop1)

    @tag('shop_types')
    def test_shop_types(self):
        url = reverse('type_of_shops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @tag('product_of_shop')
    def test_product_of_shop(self):
        url = reverse('product_of_shop', kwargs={
                      'shop_slug': self.shop1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["products"]), 2)

    @tag('shop_list')
    def test_shops(self):
        url = reverse('list_of_shops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
