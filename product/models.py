from django.db.models import Count
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from user.models import User

# Create your models here.


class Category(MPTTModel):
    STATUS = (("True", "True"), ("False", "False"))
    parent = TreeForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE
    )  # category tree
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/categories")
    status = models.CharField(max_length=10, choices=STATUS, default="True")
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.title)
    def image_tag(self):
        if self.image and hasattr(self.image, "url"):
            return mark_safe('<img src="{}" height ="50" />'.format(self.image.url))
        else:
            return ""

    image_tag.short_description = "Image"

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))

    class MPTTMeta:
        order_insertion_by = ["title"]

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
            # return ' / '.join(full_path[::-1])
        # return self.title
        return " / ".join(full_path[::-1])


class Product(models.Model):
    STATUS = (("True", "True"), ("False", "False"))

    VARIANTS = (
        ("None", "None"),
        ("Dimension", "Dimension"),
        ("Materiel", "Materiel"),
        ("Color", "Color"),
        ("Type", "Type"),
        ("Fastener", "Fastener"),
        # ('Visuel', 'Visuel'),
        ("Typologie", "Typologie"),
        ("Adehesive_Appearence", "Adehesive_Appearence"),
        ("Color-Fastner", "Color-Fastner"),
        ("Typologie-Color", "Typologie-Color"),
        ("Dimension-Materiel", "Dimension-Materiel"),
        # ('Visuel-Adehesive_Appearence', 'Visuel-Adehesive_Appearence'),
        ("Dimension-Materiel-Colors", "Dimension-Materiel-Colors"),
        # ('Dimension-Materiel-Visuel', 'Dimension-Materiel-Visuel'),
        ("Materiel-Color", "Materiel-Colorr"),
        ("Dimension-Adehesive_Appearence", "Dimension-Adehesive_Appearence"),
        ("Color-Type-Fastner", "Color-Type-Fastner"),
        ("Color-Type-Adehesive_Appearence", "Color-Type-Adehesive_Appearence"),
        ("Dimension-Materiel-Type", "Dimension-Materiel-Type"),
        (
            "Dimension-Color-Adehesive_Appearence",
            "Dimension-Materiel-Adehesive_Appearence",
        ),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    fiche = models.FileField(upload_to="product/", blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    variant = models.CharField(max_length=400, choices=VARIANTS, default="None")
    detail = RichTextUploadingField()
    visual = models.BooleanField(default=True)
    product_views = models.IntegerField(default=0)
    product_search = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))

    def image_tag(self):
        if self.image and hasattr(self.image, "url"):
            return mark_safe('<img src="{}" height ="50" />'.format(self.image.url))
        else:
            return ""

    image_tag.short_description = "Image"

    # def averagereview(self):
    #     reviews = Comment.filter(
    #         product=self, status='True').aggregate(average=Avg('rate'))
    #     avg = 0
    #     if reviews['average'] is not None:
    #         avg = float(reviews['average'])

    #     return avg

    # def counterview(self):
    #     reviews = Comment.filter(product=self).aggregate(count=Count('id'))
    #     cnt = 0
    #     if reviews['count'] is not None:
    #         cnt = int(reviews['count'])
    #     return cnt


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    STATUS = (("New", "New"), ("True", "True"), ("False", "False"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=450, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject


# variant


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))

    def color_tag(self):
        if self.code is not None:
            return mark_safe(
                '<p style="background-color:{}">{}</p>'.format(self.code, self.name)
            )
        else:
            return ""


class Demension(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))


class Materiel(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))


class Visuel(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def hash_pk(self):
        return urlsafe_base64_encode(force_bytes(self.id))


class Fastener(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Typologie(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Adehesive_Appearence(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    CHOICE = (
        ("None", "None"),
        ("Personnalise", "Personnalise"),
    )

    name = models.CharField(max_length=50, choices=CHOICE, default="None")

    def __str__(self) -> str:
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    demension = models.ForeignKey(
        Demension, on_delete=models.CASCADE, blank=True, null=True
    )
    materiel = models.ForeignKey(
        Materiel, on_delete=models.CASCADE, blank=True, null=True
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    # visuel = models.ForeignKey(
    #     Visuel, on_delete=models.CASCADE, blank=True, null=True)
    fastner = models.ForeignKey(
        Fastener, on_delete=models.CASCADE, blank=True, null=True
    )
    typologie = models.ForeignKey(
        Typologie, on_delete=models.CASCADE, blank=True, null=True
    )
    adehesive = models.ForeignKey(
        Adehesive_Appearence, on_delete=models.CASCADE, blank=True, null=True
    )
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        if self.title is not None:
            return self.title
        else:
            return ""

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class ProductVisual(models.Model):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_productvisual",
    )
    visual = models.ForeignKey(
        "product.Visuel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visual_productvisual",
    )

    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.product.title} | {self.visual.name}"
