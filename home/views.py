from django.core.paginator import Paginator, EmptyPage
from django.views.defaults import page_not_found
import json
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
import logging
from user.utils import send_email_with_html_body

from home.models import (
    FAQ,
    Banner,
    BannerSecand,
    ContactForm,
    ContactMessage,
    Rating,
    RatingForm,
    Settings,
)
from order.models import ShopCart
from product.models import Category, Product
from user.models import UserProfile
from .forms import SearchForm
from django.shortcuts import get_object_or_404

# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    # logger.warning(request, "INDEX == HOME")
    template_name = "home/index.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    settings = Settings.objects.get_or_create(
        id=1,
        defaults={
            "title": "Signalétique Solutions",
            "keywords": "Signalétique Solutions",
            "description": "signalisations",
        },
    )
    setting = settings[0]
    setting.site_views += 1
    setting.save()
    cat_set = Category.objects.filter(parent=None)
    page = "home"
    banners = Banner.objects.all()
    latest_product = Product.objects.all().order_by("-id")[:4]
    secand_banner = BannerSecand.objects.all().order_by("-id")[:3]
    products = list(Product.objects.all())

    context = {
        "cat_set": cat_set,
        "category_filter": category_filter,
        "setting": setting,
        "page": page,
        "banners": banners,
        "latest_product": latest_product,
        "secand_banner": secand_banner,
        # 'random_products': random_products
    }

    if len(products) > 0:
        qty = len(products)
        if qty < 4:
            random_products = random.sample(products, qty)
        else:
            random_products = random.sample(products, 4)

        context.update({"random_products": random_products})
    # add number of product in cart and amount and list cart
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})

    return render(request, template_name, context)
    # return HttpResponse("home", request)


def search(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]  # get form input data
            catid = form.cleaned_data["catid"]
            if catid == 0:
                # SELECT * FROM product WHERE title LIKE '%query%'
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=catid
                )

            for rs in products:
                rs.product_search += 1
                rs.save()

            setting = Settings.objects.get(id=1)
            category = Category.objects.all()

            context = {
                "products": products,
                "query": query,
                "category_filter": category,
                "setting": setting,
            }

            current_user = request.user.id
            if current_user:
                userprofile = UserProfile.objects.get(
                    user_id=current_user
                )  # to add information about cart
                shopcarts = ShopCart.objects.filter(user_id=current_user)
                context.update({"shopcarts": shopcarts, "userprofile": userprofile})
            return render(request, "home/search_products.html", context)

    return HttpResponseRedirect("/")


def search_auto(request):
    print(f"$$$$$ PRODUCTS search_auto ")
    if request.is_ajax():
        q = request.GET.get("term", "")
        print(f"--- is ajax")
        products = Product.objects.filter(title__icontains=q)
        print(f"$$$$$ PRODUCTS {products}")

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title  # + " > " + rs.category.title
            results.append(product_json)
            data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    print("------------------ajax")
    return HttpResponse(data, mimetype)


def error_500(request):
    template_name = "home/500.html"
    return render(request, template_name, status=500)


def error_404(request, exception):
    template_name = "home/404.html"
    return page_not_found(request, exception, template_name)
    # return render(request, template_name, status=404)


def contactus(request):
    template_name = "home/contactus.html"
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data["name"]
            data.email = form.cleaned_data["email"]
            data.subject = form.cleaned_data["subject"]
            data.message = form.cleaned_data["message"]
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            messages.success(
                request, "Your message has ben sent. Thank you for your message."
            )
            return HttpResponseRedirect("/contactus")

    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        # 'cat_set': cat_set,
        "form": form,
    }
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)


def faq(request):
    template_name = "home/faq.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        "faq": faq,
        # 'cat_set': cat_set,
    }

    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)


# @login_required(login_url="profile:login")
def rating(request):
    template_name = "home/rating.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    ratings = Rating.objects.filter(status="True")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(ratings, 3)
    try:
        ratings = paginator.page(page_number)
    except EmptyPage:
        ratings = paginator.page(paginator.num_pages)

    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        "ratings": ratings,
        "paginator": paginator,
        # 'cat_set': cat_set,
    }

    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)


def addReview(request):
    url = request.META.get("HTTP_REFERER")  # get last url
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            data = Rating()
            current_user = request.user
            data.user_id = current_user.id
            data.subject = form.cleaned_data["subject"]
            data.comment = form.cleaned_data["comment"]
            data.rate = form.cleaned_data["rate"]
            data.ip = request.META.get("REMOTE_ADDR")
            data.status = "True"
            data.save()
            messages.success(
                request, "Your review has ben sent. Thank you for your interest."
            )
            return HttpResponseRedirect(url)

        return HttpResponseRedirect(url)


def aboutus(request):
    template_name = "home/aboutus.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        # 'cat_set': cat_set,
    }
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)
