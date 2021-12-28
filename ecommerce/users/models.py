from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from datetime import datetime

# Create your models here.


class CustomUser(AbstractUser):
    CUSTOMER = 'CT'
    SUPLIER='SL'
    ADMIN='AD'
    USER_TYPE= (
            (CUSTOMER, 'Customer'),
            (SUPLIER, 'Suplier'),
            (ADMIN,'Admin'),
    )
    REQUIRED_FIELDS = ['email']
    user_type =models.CharField(choices=USER_TYPE, default=CUSTOMER, max_length=2,) 
    # email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20)
    address =  models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    city=models.CharField(max_length=25 , null=True ,blank=True)
    zip=models.CharField(max_length=100 , null=True ,blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)



    objects = CustomUserManager()

    def __str__(self):
        return self.email