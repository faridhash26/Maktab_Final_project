from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Shop(models.Model):
    shop_type = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    is_active=models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
