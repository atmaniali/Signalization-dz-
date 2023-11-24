from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from ckeditor_uploader.fields import RichTextUploadingField

from user.models import User


# Create your models here.
class Settings(models.Model):
    STATUS = (("True", "True"), ("False", "False"))
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(blank=True, null=True, max_length=150)
    phone = models.CharField(blank=True, null=True, max_length=15)
    fax = models.CharField(blank=True, null=True, max_length=15)
    fax = models.CharField(blank=True, null=True, max_length=50)
    smtpserver = models.CharField(blank=True, null=True, max_length=50)
    smtpemail = models.CharField(blank=True, null=True, max_length=50)
    smtppassword = models.CharField(blank=True, null=True, max_length=10)
    smtpport = models.CharField(blank=True, null=True, max_length=5)
    icon = models.ImageField(blank=True, null=True, upload_to="images/")
    logo = models.ImageField(blank=True, null=True, upload_to="images/")
    facebook = models.CharField(blank=True, null=True, max_length=150)
    instgram = models.CharField(blank=True, null=True, max_length=150)
    twitter = models.CharField(blank=True, null=True, max_length=150)
    linkdin = models.CharField(blank=True, null=True, max_length=150)
    whatsapp = models.CharField(blank=True, null=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True, null=True)
    contact = RichTextUploadingField(blank=True, null=True)
    references = RichTextUploadingField(blank=True, null=True)
    site_views = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default="True")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "setting"
        verbose_name_plural = "settings"


class ContactMessage(models.Model):
    STATUS = (
        ("New", "New"),
        ("Read", "Read"),
        ("Closed", "Closed"),
    )
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": TextInput(attrs={"class": "input", "placeholder": "Nom & Prénom"}),
            "subject": TextInput(attrs={"class": "input", "placeholder": "Sujet"}),
            "email": TextInput(
                attrs={"class": "input", "placeholder": "Email Address"}
            ),
            "message": Textarea(
                attrs={
                    "class": "input",
                    "placeholder": "Votre message",
                    "rows": 80,
                    "cols": 20,
                }
            ),
        }
        labels = {
            "name": "nom et prénom",
            "subject": "sujet",
        }


class FAQ(models.Model):
    STATUS = (("True", "True"), ("False", "False"))
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default="True")

    def __str__(self):
        return self.question


class Rating(models.Model):
    STATUS = (
        ("New", "New"),
        ("True", "True"),
        ("False", "False"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ["subject", "comment", "rate"]
        labels = {
            "subject": "sujet",
            "comment": "commentaire",
            "rate": "rate",
        }


class Banner(models.Model):
    STATUS = (("True", "True"), ("False", "False"))

    CLASES = (
        ("white-color font-weak", "white-color font-weak"),
        ("white-color", "white-color"),
        ("None", "None"),
        ("primary-color", "primary-color"),
    )

    main_title = models.CharField(max_length=250, blank=True, null=True)
    secand_title = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="images/banners")
    status = models.CharField(max_length=10, choices=STATUS, default="True")
    main_title_clases = models.CharField(max_length=100, choices=CLASES, default="None")
    secand_title_clases = models.CharField(
        max_length=100, choices=CLASES, default="None"
    )


class BannerSecand(models.Model):
    STATUS = (("True", "True"), ("False", "False"))

    CLASES = (
        ("white-color font-weak", "white-color font-weak"),
        ("white-color", "white-color"),
        ("None", "None"),
        ("primary-color", "primary-color"),
    )

    main_title = models.CharField(max_length=250, blank=True, null=True)
    secand_title = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="images/banners")
    status = models.CharField(max_length=10, choices=STATUS, default="True")
    main_title_clases = models.CharField(max_length=100, choices=CLASES, default="None")
    secand_title_clases = models.CharField(
        max_length=100, choices=CLASES, default="None"
    )
