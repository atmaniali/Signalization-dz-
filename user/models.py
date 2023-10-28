from django.db import models
from django.utils.html import mark_safe
from django.db.models import Count, Sum
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):  # new
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):  # new
    """User Model"""

    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    # city = models.CharField(blank=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # objects = UserManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(
        default="images/users/img1.jpg",
        upload_to="images/users/",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.user.email

    def email(self):
        return self.user.email

    def user_name(self):
        return self.user.username

    def image_tag(self):
        return mark_safe('<img src="{}" height ="50" />'.format(self.image.url))

    image_tag.short_description = "Image"

    def countcard(self):
        count = self.user.userShopCart.all().aggregate(count=Count("id"))
        cnt = 0
        if count["count"] is not None:
            cnt = count["count"]
        return cnt

    def amountcard(self):
        sum = self.user.userShopCart.all()
        amount = 0
        for obj in sum:
            # print(f"MODELS {obj}")
            if obj.product.variant == "None":
                amount += float(obj.amount)
            else:
                if obj.variant == None:
                    amount += float(obj.amount)
                else:
                    amount += float(obj.varamount)

        return amount
