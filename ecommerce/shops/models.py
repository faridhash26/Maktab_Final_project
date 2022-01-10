from django.db import models
from django.contrib.auth import get_user_model
import random
import string
from django.utils.text import slugify
# Create your models here.

User = get_user_model()


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slugify(instance, slug):
    """
    checking if slug exist adding string to slug
    """
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug
        unique_slug += random_string_generator(size=4)
    return unique_slug


class Shop(models.Model):
    SUP = "SUP"
    HYP = "HYP"
    BAK = "BAKERY"
    FRU = "FRUIT"
    BOOK = "BOOKSHOP"
    TYPE_CHOICES = (
        (SUP, "Supermarket"),
        (HYP, "Hypermarket"),
        (BAK, "Bakery"),
        (FRU, "fruit store"),
        (BOOK, "Bookshop")
    )
    shop_type = models.CharField(max_length=17, choices=TYPE_CHOICES, default=SUP)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    is_active=models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
