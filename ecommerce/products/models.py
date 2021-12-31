from django.db import models
from django.utils.text import slugify
import random
import string
from django.contrib.auth import get_user_model
from shops.models import Shop

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


class Category(models.Model):
    title = models.CharField('category title ', max_length=40)
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    title = models.CharField('tite', max_length=255)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "tags"
        verbose_name = "tag"
        db_table = 'tag'
        ordering = ['-title', ]

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    price =models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    weight = models.DecimalField(max_digits=5 , decimal_places=2 ,null=True, blank=True)
    stock = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    is_published=models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField('comment title')
    create_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.text[:10]} - {self.post}'
