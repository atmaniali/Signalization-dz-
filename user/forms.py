# from fileinput import FileInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.forms import TextInput, EmailInput, FileInput

from user.models import User, UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="User Name :")
    email = forms.EmailField(max_length=100, required=False, label="Email :")
    first_name = forms.CharField(label="First Name :", max_length=100, required=False)
    lastname = forms.CharField(label="Last Name :", max_length=100, required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
        labels = {"first_name": "Prénom", "last_name": "Nom"}


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username", "last_name", "first_name")
        widgets = {
            # 'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            "email": EmailInput(attrs={"class": "input", "placeholder": "email"}),
            "username": TextInput(attrs={"class": "input", "placeholder": "username"}),
            "first_name": TextInput(attrs={"class": "input", "placeholder": "prenom"}),
            "last_name": TextInput(attrs={"class": "input", "placeholder": "nom"}),
        }
        labels = {"first_name": "Prénom", "last_name": "Nom"}


CITY = [
    ("Istanbul", "Istanbul"),
    ("Ankara", "Ankara"),
    ("Izmir", "Izmir"),
    # ("Istanbul", "Istanbul"),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "address", "city", "country", "image")
        widgets = {
            "phone": TextInput(attrs={"class": "input", "placeholder": "phone"}),
            "address": TextInput(attrs={"class": "input", "placeholder": "address"}),
            # 'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            "city": TextInput(attrs={"class": "input", "placeholder": "city"}),
            "country": TextInput(attrs={"class": "input", "placeholder": "country"}),
            "image": FileInput(attrs={"class": "input", "placeholder": "image"}),
        }
        labels = {
            "phone": "Téléphone",
            "city": "ville",
            "country": "pays",
        }
