from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from django.test import tag
from django.urls import reverse
from rest_framework import status

from products.models import Product
from users.models import CustomUser
from .models import Order,OrderItem
from shops.models import Shop


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
        self.product1 = mommy.make(Product, shop=self.shop1,price=10 ,stock=6)
        self.product2 = mommy.make(Product, shop=self.shop1,price=12 ,stock=5)
        self.client.force_authenticate(self.customer1)
        self.order1 = mommy.make(Order,customer=self.customer1 ) 
        self.orderitem1=mommy.make(OrderItem,order=self.order1 , product=self.product1 )

    # @tag('ordering')
    # def test_create_order(self):
    #     print(self.product1.id)
    #     new_order = {"order_of_orderitem": [{"product": self.product1.id,"qty": 1}]}
    #     url = reverse('orders:new_order_api')
    #     response = self.client.post(url, data=new_order)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('update_order')
    def test_updating_orderitem(self):
      
      url = reverse('orders:updating_order_item',kwargs={'pk': self.order1.id})
      data ={"product":self.product2.id,"qty":1}
      response = self.client.post(url ,data=data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('delete_orderitem')
    def test_updating_orderitem(self):
      url = reverse('orders:delete_order_item',kwargs={'order_id': self.order1.id , "orderitem_id":self.orderitem1.id})
      response = self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      url = reverse('orders:list_processing')
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 0)


    @tag('paying_order')
    def test_paying_order(self):
      url = reverse('orders:paying_order',kwargs={'order_id': self.order1.id})
      response = self.client.put(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data["status"],"PD")



    @tag('allprocessing')
    def test_processing_order(self):
      url = reverse('orders:list_processing')
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 1)


    @tag('all_order_paid')
    def test_paid_order(self):
      url_pay = reverse('orders:paying_order',kwargs={'order_id': self.order1.id})
      response_pay = self.client.put(url_pay)
      self.assertEqual(response_pay.status_code, status.HTTP_200_OK)
      url = reverse('orders:paid_list')
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 1)


