from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Sum,Count,Max

from orders.models import Order,OrderItem
from orders.serializers import OrderSerializer, PaymentShopSerializer,UpdateOrderItem
from products.models import Product






class CreateOrderByCustomer(generics.CreateAPIView):
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class=OrderSerializer



class UpdateTheOrderItem(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=UpdateOrderItem
    model = OrderItem

class DeleteOrderItem(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = OrderItem

    def destroy(self, request, *args, **kwargs):

        order_of_item=  get_object_or_404(OrderItem , id =kwargs["orderitem_id"])
        if order_of_item.order.status == 'PS':
            the_product = get_object_or_404(Product ,id= order_of_item.product.id)
            the_product.stock = the_product.stock +order_of_item.qty
            the_product.save()
            order_of_item.delete()

            try:
                order_items_count= OrderItem.objects.filter(order=kwargs["order_id"]).count()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            if order_items_count==0:
                Order.objects.get(id =kwargs["order_id"]).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response( {"error":"you can just delete item when status is processing!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




class Paymentview(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    model=Order
    queryset=Order.objects.all()
    lookup_field="id"
    lookup_url_kwarg="order_id"
    serializer_class=PaymentShopSerializer

    def put(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk = kwargs["order_id"])
        except:
            return Response(  status=status.HTTP_404_NOT_FOUND)

        total_price =  OrderItem.objects.filter(order=order.id).aggregate(Sum('price'))       
        if order.status  == "PS":
            order.status = 'PD'
            if order.taxPrice:
                order.totalPrice = total_price["price__sum"]+order.taxPrice
            else:
                order.totalPrice = total_price["price__sum"]
            order.save()
            
            return self.update(request, *args, **kwargs)
        return Response(  {"error" :"you dont have permision to payment !"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ListOfProcessingOrderMethod(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=PaymentShopSerializer
    model=Order
    def get_queryset(self):
        return self.model.objects.filter(status="PS" ,customer=self.request.user.id)


class ListOfPaid(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=PaymentShopSerializer
    model=Order
    def get_queryset(self):
        return self.model.objects.filter(status="PD" ,customer=self.request.user.id)
