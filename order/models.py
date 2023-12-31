from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.timezone import now
from datetime import datetime
from django.db import models


from product.models import Product, Variants
from user.models import User


# Create your models here.
class ShopCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="userShopCart"
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True
    )  # relation with varinat
    quantity = models.IntegerField()
    visual = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return float(self.product.price)

    @property
    def varprice(self):
        if self.variant is None:
            return 0
        return float(self.variant.price)

    @property
    def amount(self):
        return float(self.quantity * self.product.price)

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))

    @property
    def varamount(self):
        return self.quantity * self.variant.price


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Preaparing", "Preaparing"),
        ("OnShipping", "OnShipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    # country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # TODO: hadi zidha fl main project
        return str(self.user)

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))


# order details model
class OrderProduct(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        Variants, on_delete=models.CASCADE, blank=True, null=True
    )  # relation with varinat
    quantity = models.IntegerField()
    visual = models.CharField(max_length=300, blank=True, null=True)
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))


class LikedList(models.Model):
    STATUS = (
        ("Like", "Like"),
        ("Dislike", "Dislike"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default="Like")
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return self.status

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))
