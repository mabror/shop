from django.db import models
from django.contrib.auth import get_user_model
from django.utils import translation

User = get_user_model()
from decimal import *
from PIL import Image
from io import BytesIO
from django.core.files import File
import string, random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.conf import settings
from django.utils.translation import get_language


class Category(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


category_list = ['a', 'd', 'k', 'b', 'c', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'i', 'l', 'z']


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "_" + str(random.choice(category_list)))


class Brand(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', models.CASCADE)

    def __str__(self):
        return self.name


brand_list = ['a', 'd', 'k', 'b', 'c', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'i', 'l', 'z']


@receiver(pre_save, sender=Brand)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "_" + str(random.choice(brand_list)))


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True)
    name_en = models.CharField(max_length=200, null=True, blank=True)
    name_ru = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='shop_product/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0, null=True, blank=True)
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    warranty = models.CharField(max_length=250, null=True, blank=True)
    return_policy = models.CharField(max_length=250, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    countInstok = models.IntegerField(default=0, blank=True, null=True)
    createDat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.image.closed:
            img = Image.open(self.image)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.image = File(tmp, 'image.png')
        return super().save(*args, **kwargs)
    
    @property
    def name(self):
        column = 'name_{}'.format(get_language())
        return getattr(self, column)


str_list = ['a', 'd', 'k', 'b', 'c', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'i', 'l', 'z']


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "_" + str(random.choice(str_list)))


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(default=0, blank=True, null=True)
    comment = models.TextField()

    def __str__(self):
        return str(self.rating)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart" + str(self.id)

    def get_amount(self):
        return self.total * 100


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart" + str(self.cart_id) + "CartProduct" + str(self.id)


ORDER_STATUS = (
    ("Buyurtma qabul qilindi", "Buyurtma qabul qilindi"),
    ("Buyurtmani qayta ishlash", "Buyurtmani qayta ishlash"),
    ("Yo'lda", "Yo'lda"),
    ("Buyurtma bajarildi", "Buyurtma bajarildi"),
    ("Buyurtma bekor qilindi", "Buyurtma bekor qilindi")
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="Shahar / Viloyat")
    district = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tuman")
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ko'cha")
    house_number = models.IntegerField(blank=True, null=True, verbose_name="Uy nomeri")
    phone = models.CharField(max_length=14, verbose_name="Telefon Nomer")
    email = models.EmailField(null=True, blank=True, verbose_name="Elektron Pochta")
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=250, default=1, choices=ORDER_STATUS)
    createdAt = models.DateTimeField(auto_now_add=True)



