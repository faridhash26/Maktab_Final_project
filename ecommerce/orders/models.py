from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Order(models.Model):
    CONFIRM ='CF'
    PROCESSING = 'PS'
    PAID='PD'
    CANCEL='CN'
    STATUS_CHOICES = (
            (CONFIRM, 'Confirm'),
            (PROCESSING, 'Processing'),
            (PAID, 'Paid'),
            (CANCEL, 'Cancel'),
    )
    status =models.CharField(max_length=2,choices=STATUS_CHOICES,default=PROCESSING) 

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    taxPrice = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    
    def __str__(self):
        return f'{self.createdAt}  -   {self.customer}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True ,related_name="order_of_orderitem")
    qty = models.PositiveIntegerField(null=True, blank=True, default=1)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    price =models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)


    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.qty
        return super().save(*args, **kwargs)