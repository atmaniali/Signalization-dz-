from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from order.models import LikedList, Order, OrderProduct, ShopCart
from product.models import Category, Variants

from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm
from home.models import Settings
from user.models import User, UserProfile
from user.utils import send_email_with_html_body

import logging

logger = logging.getLogger(__name__)

# Create your views here.


@login_required(login_url="profile:login")  # Check login
def index(request):
    template_name = "user/user/user_profile.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        "userprofile": profile,
        # 'form': form,
    }
    return render(request, template_name, context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def login_user(request):
    template_name = "user/user/login_form.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    cat_set = Category.objects.filter(parent=None)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            if userprofile.image:
                request.session["userimage"] = userprofile.image.url
            return HttpResponseRedirect("/")
        else:
            messages.warning(request, "Login Error !! Email or Password is incorrect")
            return HttpResponseRedirect("/user/login")
    context = {
        "category_filter": category_filter,
        "setting": setting,
        # 'cat_set': cat_set,
    }
    return render(request, template_name, context)
    # return HttpResponse('/ login')


def register_user(request):
    template_name = "user/user/signup_form.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    # numero = setting.phone
    # form = SignUpForm(request.POST or None)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")  # with todo
            user = authenticate(request, email=email, password=password)
            user.username = username
            user.save()
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.save()
            logger.info("🥸 creation of user")
            print("🎯 Registration user ")
            # TODO send mail registration
            subject = "Creation d'un compte signalitique-solutions"
            template = "user/email/registration_mail.html"
            # user / email / registration_mail.html
            site = "https://%s/" % (Site.objects.get_current().domain)
            ctx = {
                "email": email,
                "date": datetime.today().date,
                "user_name": username,
                "numero": "09",
                "site": site,
                "setting": setting,
            }
            # "user_name": "user name",
            # "numero": "0668999985",
            receivers = [email]
            print(
                f" function mail prepar 💖 subject : {subject} "
                f"\t context {ctx} \t receivers {receivers} \t template {1}"
            )
            has_send = send_email_with_html_body(
                subjet=subject, context=ctx, recevers=receivers, template=template
            )  #
            if has_send:
                # TODO added but not tested
                messages.success(request, "Your account has been created!")
                return HttpResponseRedirect("/")

            # messages.success(request, 'Your account has been created!')
            # return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/user/register")
    # current_user = request.user
    # profile = UserProfile.objects.get(user_id=current_user.id)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        # 'cat_set': cat_set,
        # 'userprofile': profile,
        # 'form': form,
    }
    return render(request, template_name, context)
    # return HttpResponse('/ register')


@login_required(login_url="profile:login")
def user_update(request):
    template_name = "user/user/user_update.html"
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated!")
            return HttpResponseRedirect("/user/")
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        setting = Settings.objects.get(id=1)
        cat_set = Category.objects.filter(parent=None)
        context = {
            "category_filter": category,
            "user_form": user_form,
            "profile_form": profile_form,
            "userprofile": profile,
            # 'cat_set': cat_set,
            "setting": setting,
        }
        return render(request, template_name, context)


# TODO add " | safe " to all messages in template


@login_required(login_url="profile:login")
def user_password(request):
    """
    function change password user by propose 3 fields old password new password and confirmation password
    """
    template_name = "user/user/user_password.html"
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return HttpResponseRedirect("/user")
        else:
            messages.error(
                request, "Please correct the error below.<br>" + str(form.errors)
            )
            return HttpResponseRedirect("/user/password")

    else:
        form = PasswordChangeForm(request.user)
        category = Category.objects.all()
        setting = Settings.objects.get(id=1)
        cat_set = Category.objects.filter(parent=None)
        context = {
            "category_filter": category,
            "form": form,
            # 'cat_set': cat_set,
            # 'profile_form': profile_form,
            "setting": setting,
        }
        return render(request, template_name, context)
    # return HttpResponse('password changed! ')


def reset_password(request):
    """
    function verifie if email user exist
    """
    template_name = "user/user/reset_password.html"
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Reset Password"
            recevers = [email]
            template = "user/email/reset_password.html"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = uuid.uuid4()
            current_datetime = datetime.now()
            # 'http://127.0.0.1:8000'
            site = "https://%s/" % (Site.objects.get_current().domain)
            ctx = {
                "token": token,
                "uidb64": uidb64,
                "setting": setting,
                "site": site,
                "current_datetime": current_datetime,
            }
            print("mail sent start")
            send_email_with_html_body(
                subjet=subject, recevers=recevers, template=template, context=ctx
            )
            print("mail sent end")
            messages.success(request, "cheak your email ")
            return HttpResponseRedirect("/user/done")
        else:
            messages.error(request, "Mail does not exist.<br>")
            return HttpResponseRedirect("/user/reset")

    cat_set = Category.objects.filter(parent=None)
    context = {
        "setting": setting,
        "category_filter": category,
        # 'cat_set': cat_set,
    }
    return render(request, template_name, context)


def email_sent_done(request):
    """
    help to send email after verification email of user
    """
    template_name = "user/user/email_sent_done.html"
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "setting": setting,
        "category_filter": category,
        # 'cat_set': cat_set,
    }
    return render(request, template_name, context)


def change_password(request, uidb64, token):
    """
    this function it's send url for user how forget password
    """
    url = request.META.get("HTTP_REFERER")
    template_name = "user/user/user_forget_password.html"
    print(" 😵😵 uidb64 ", uidb64)
    user_id = force_str(urlsafe_base64_decode(uidb64))
    # user_id = int
    user = User.objects.get(pk=user_id)
    # user = User.objects.get(pk=1)
    # form = SetPasswordForm(user)
    # return HttpResponse(form)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user_form = form.save()
            # update_session_auth_hash(user_form)
            messages.success(
                request, "Your password was successfully updated! you should login "
            )
            return HttpResponseRedirect("/user/login")
        else:
            messages.error(
                request, "Please correct the error below.<br>" + str(form.errors)
            )
            return HttpResponseRedirect(url)

    else:
        form = SetPasswordForm(user)
        category = Category.objects.all()
        setting = Settings.objects.get(id=1)
        cat_set = Category.objects.filter(parent=None)
        context = {
            "category_filter": category,
            "form": form,
            # 'cat_set': cat_set,
            # 'profile_form': profile_form,
            "setting": setting,
        }
        return render(request, template_name, context)


@login_required(login_url="profile:login")
def user_order(request):
    template_name = "user/user/user_order.html"
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    current_user = request.user.id
    orders = Order.objects.filter(user_id=current_user)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category,
        "setting": setting,
        # 'cat_set': cat_set,
        "orders": orders,
    }
    # TODO verifie if added in all page needed
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update(
            {
                "shopcarts": shopcarts,
                "userprofile": userprofile,
            }
        )
    return render(request, template_name, context)


@login_required(login_url="profile:login")
def user_order_detail(request, id):
    template_name = "user/user/user_order_detail.html"
    order_id = force_str(urlsafe_base64_decode(id))
    current_user = request.user
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    order = Order.objects.get(user_id=current_user.id, id=order_id)
    orderitems = OrderProduct.objects.filter(order_id=order_id)
    cat_set = Category.objects.filter(parent=None)
    context = {
        # 'category': category,
        "order": order,
        "orderitems": orderitems,
        "category_filter": category,
        "setting": setting,
        # 'cat_set': cat_set,
    }
    userprofile = UserProfile.objects.get(
        user_id=current_user
    )  # to add information about cart
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    context.update(
        {
            "shopcarts": shopcarts,
            "userprofile": userprofile,
        }
    )

    return render(request, template_name, context)


# TODO check header > acount/cart
# TODO add caches  and  seo pluging admin-fake and session timer logout


@login_required(login_url="profile:login")
def user_order_product(request):
    template_name = "user/user/user_order_products.html"
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by("-id")
    context = {  # 'category': category,
        "order_product": order_product,
    }
    userprofile = UserProfile.objects.get(
        user_id=current_user
    )  # to add information about cart
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    cat_set = Category.objects.filter(parent=None)
    context.update(
        {
            "shopcarts": shopcarts,
            "userprofile": userprofile,
            "category_filter": category,
            "setting": setting,
            # 'cat_set': cat_set,
        }
    )
    return render(request, template_name, context)


@login_required(login_url="/profile:login")  # Check login
def user_order_product_detail(request, id, oid):
    template_name = "user/user/user_order_detail.html"
    order_id = force_str(urlsafe_base64_decode(oid))
    order_product_id = force_str(urlsafe_base64_decode(id))
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=order_id)
    orderitems = OrderProduct.objects.filter(
        id=order_product_id, user_id=current_user.id
    )
    cat_set = Category.objects.filter(parent=None)
    context = {
        # 'category': category,
        "order": order,
        "orderitems": orderitems,
        # 'cat_set': cat_set,
    }
    # if orderitems.variant_id is not None:
    #     variant = Variants.objects.get(id=orderitems.variant_id)
    #     context.update({'variant': variant})
    userprofile = UserProfile.objects.get(
        user_id=current_user
    )  # to add information about cart
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    context.update(
        {
            "shopcarts": shopcarts,
            "userprofile": userprofile,
            "category_filter": category,
            "setting": setting,
        }
    )

    return render(request, template_name, context)


@login_required(login_url="profile:login")
def user_likedproduct(request):
    template_name = "user/user/favorit.html"
    current_user = request.user
    userprofile = UserProfile.objects.get(
        user_id=current_user
    )  # to add information about cart
    shopcarts = ShopCart.objects.filter(user_id=current_user)
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    liked = LikedList.objects.filter(user_id=current_user.id)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "liked": liked,
        "category_filter": category_filter,
        "setting": setting,
        "shopcarts": shopcarts,
        # 'cat_set': cat_set,
        "userprofile": userprofile,
    }
    return render(request, template_name, context)


@login_required(login_url="profile:login")
def delete_favorit(request, id):
    url = request.META.get("HTTP_REFERER")
    fav_id = force_str(urlsafe_base64_decode(id))
    LikedList.objects.filter(id=fav_id).delete()
    messages.success(request, "Your item deleted form Favorit.")
    return HttpResponseRedirect(url)


def test_mail_template(request):
    context = {
        "user_name": "user name",
        "numero": "0668999985",
        "email": "atmaniali97@gmail.com",
    }
    template = "user/email/registration_mail.html"
    return render(request, template, context)
