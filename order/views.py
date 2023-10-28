import datetime
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from home.models import Settings
from order.models import LikedList, Order, OrderProduct, ShopCart
from product.models import Category, Product, Variants
from user.models import UserProfile
from user.utils import send_email_with_html_body
from .forms import ShopCartForm, OrderForm

# Create your views here.


@login_required(login_url="profile:login")
def shopcart(request):
    template_name = "order/index.html"
    # shopcart = ShopCart.objects.filter(user_id=request.user.id)
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    cat_set = Category.objects.filter(parent=None)
    context = {
        # 'shopcart': shopcart,
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


@login_required(login_url="profile:login")
def shopcartdetail(request, id):
    shopcart_id = force_str(urlsafe_base64_decode(id))
    template_name = "order/shopcart_detail.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    shopcart = ShopCart.objects.get(id=shopcart_id)
    product = Product.objects.get(id=shopcart.product_id)
    cat_set = Category.objects.filter(parent=None)
    context = {
        # 'shopcart': shopcart,
        "category_filter": category_filter,
        "setting": setting,
        # 'cat_set': cat_set,
        "product": product,
    }
    if product.variant != "None" and shopcart.variant is not None:
        variant = Variants.objects.get(id=shopcart.variant_id)
        context.update({"variant": variant})
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
        return render(request, template_name, context)


def deletefromcart(request, id):
    url = request.META.get("HTTP_REFERER")
    shopcart_id = force_str(urlsafe_base64_decode(id))
    ShopCart.objects.filter(id=shopcart_id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect(url)


@login_required(login_url="profile:login")
def orderproduct(request):
    template_name = "order/order_product.html"  # TODO add to templates
    current_user = request.user
    category = Category.objects.all()
    setting = Settings.objects.get(id=1)
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    # return HttpResponse("post")
    if request.method == "POST":
        print("post methode__")
        # return HttpResponse("post")
        # Send credit card to bank and get result if return info it's ok continue
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            name = (
                form.cleaned_data["first_name"] + " " + form.cleaned_data["last_name"]
            )
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.address = form.cleaned_data["address"]
            data.phone = form.cleaned_data["phone"]
            data.city = form.cleaned_data["city"]
            data.user_id = current_user.id
            data.total = profile.amountcard()
            data.ip = request.META.get("REMOTE_ADDR")
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            # print(f"----------------------------------- : {data}")
            data.save()

            # Move Shopcart items to Order Products  items
            shopcart = ShopCart.objects.filter(user_id=current_user)
            for rs in shopcart:
                # print(f"================================ : {rs}")
                detail = OrderProduct()
                detail.order_id = data.id  # Order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.variant_id = rs.variant_id
                detail.visual = rs.visual
                if rs.variant_id:
                    prix = rs.varprice
                    amount = rs.varamount
                else:
                    prix = rs.price
                    amount = rs.amount
                detail.price = prix
                detail.amount = amount
                detail.save()
                # Reduce quantity of sold product from of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                # ************** <> **********
            # Clear & Delete Shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session["cart_item"] = 0
            # TODO send email of order completed
            subject = "Order Confirmation"
            email = current_user.email
            # 'https://%s/' % (Site.objects.get_current().domain)
            site = "https://%s/" % (Site.objects.get_current().domain)
            recevers = [email]
            template = "email/order_email.html"
            orders = OrderProduct.objects.filter(
                user_id=current_user.id, order_id=data.id
            )
            total = data.total
            current_datetime = datetime.datetime.now()

            ctx = {
                "ordercode": ordercode,
                "setting": setting,
                "orders": orders,
                "name": name,
                "site": site,
                "total": total,
                "current_datetime": current_datetime,
            }
            send_email_with_html_body(
                subjet=subject, recevers=recevers, template=template, context=ctx
            )
            messages.success(request, "Your Order Has been Compleeted. Thank You")
            return render(
                request,
                "order/order_completed.html",
                {
                    "ordercode": ordercode,
                    "category_filter": category,
                    "setting": setting,
                    "userprofile": profile,
                },
            )

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("order:orderproduct")

    form = OrderForm()
    # shopcarts= ShopCart.objects.filter(user_id=current_user.id)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category,
        "shopcarts": shopcarts,
        # 'total': total,
        "form": form,
        # 'cat_set': cat_set,
        "userprofile": profile,
        "setting": setting,
    }
    return render(request, template_name, context)

    # return HttpResponse('orderproduct')


@login_required(login_url="profile:login")
def addtoshopcart(request, id):
    URL = request.META.get("HTTP_REFERER")  # get last url
    current_user = request.user  # access user session information
    # print("______ ____ current user", current_user)
    product = Product.objects.get(pk=id)
    if product.variant != "None":
        variant = Variants.objects.filter(product_id=id)[0]
        checkinvariant = ShopCart.objects.filter(
            variant_id=variant.id, user_id=current_user.id
        )
        if checkinvariant:
            control = 1
        else:
            control = 0
    else:
        checkinproduct = ShopCart.objects.filter(
            product_id=id, user_id=current_user.id
        )  # Check product in shopcart
        if checkinproduct:
            control = 1
        else:
            control = 0

    # request
    if request.method == "POST":
        if product.variant != "None":
            # all variants fields
            colors_id = request.POST.get("colors")
            materiel_id = request.POST.get("materiels")
            demension_id = request.POST.get("dimension")
            adehesive_id = request.POST.get("adehesives")
            typologie_id = request.POST.get("typologie")
            # visuel_id = request.POST.get('visuel')
            fastner_id = request.POST.get("fastner")
            type_id = request.POST.get("type")
            # print(f'********* 1  {request.POST}')

            # variant = Dimension-Color-Adehesive_Appearence
            if product.variant == "Dimension-Color-Adehesive_Appearence":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    demension_id=demension_id,
                    colors_id=colors_id,
                    adehesive_id=adehesive_id,
                )

            # variant = Dimension-Materiel-Visuel-Type
            if product.variant == "Dimension-Materiel-Type":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    demension_id=demension_id,
                    materiel_id=materiel_id,
                    type_id=type_id,
                )

            # variant = Color-Type-Adehesive_Appearence
            if product.variant == "Color-Type-Adehesive_Appearence":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    color_id=colors_id,
                    type_id=type_id,
                    adehesive_id=adehesive_id,
                )

            # variant = Color-Type-Fastner
            if product.variant == "Color-Type-Fastner":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    color_id=colors_id,
                    type_id=type_id,
                    fastner_id=fastner_id,
                )

            # variant = Dimension-Visuel-Adehesive_Appearence
            if product.variant == "Dimension-Adehesive_Appearence":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    demension_id=demension_id,
                    adehesive_id=adehesive_id,
                )

            # variant = Materiel-Visuel-Color
            if product.variant == "Materiel-Color":
                variant = get_object_or_404(
                    Variants, product_id=id, color_id=colors_id, materiel_id=materiel_id
                )
            if product.variant == "Dimension-Materiel-Colors":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    color_id=colors_id,
                    demension_id=demension_id,
                    materiel_id=materiel_id,
                )

            # variant =  Typologie-Color
            elif product.variant == "Typologie-Color":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    color_id=colors_id,
                    typologie_id=typologie_id,
                )

            # variant =  Color-Fastner
            elif product.variant == "Color-Fastner":
                variant = get_object_or_404(
                    Variants, product_id=id, color_id=colors_id, fastner_id=fastner_id
                )

            # variant =  Dimension-Materiel
            elif product.variant == "Dimension-Materiel":
                variant = get_object_or_404(
                    Variants,
                    product_id=id,
                    demension_id=demension_id,
                    materiel_id=materiel_id,
                )
                # print(f"#### VARIANT IN DIMENSION {variant}, {variant.id}")

            #   variant = Type
            elif product.variant == "Type":
                variant = get_object_or_404(Variants, product_id=id, type_id=type_id)

            #   variant = Fastener
            elif product.variant == "Fastener":
                variant = get_object_or_404(
                    Variants, product_id=id, fastner_id=fastner_id
                )
            elif product.variant == "Typologie":
                variant = get_object_or_404(
                    Variants, product_id=id, typologie_id=typologie_id
                )

            #   variant = Adehesive_Appearence
            elif product.variant == "Adehesive_Appearence":
                variant = get_object_or_404(
                    Variants, product_id=id, adehesive=adehesive_id
                )

            # variant = Color
            elif product.variant == "Color":
                variant = get_object_or_404(Variants, product_id=id, color_id=colors_id)

            # variant = Dimension
            elif product.variant == "Dimension":
                variant = get_object_or_404(
                    Variants, product_id=id, demension_id=demension_id
                )

            # variant = Materiel
            elif product.variant == "Materiel":
                variant = get_object_or_404(
                    Variants, product_id=id, materiel_id=materiel_id
                )
            checkinvariant = ShopCart.objects.filter(
                variant_id=variant.id, user_id=current_user.id
            )
            if checkinvariant:
                control = 1
            else:
                control = 0

        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == "None":
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(
                        product_id=id, variant_id=variant.id, user_id=current_user.id
                    )
                data.quantity += form.cleaned_data["quantity"]
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                if product.variant == "None":
                    data.variant_id = None
                else:
                    data.variant_id = variant.id
                data.quantity = form.cleaned_data["quantity"]
                data.visual = form.cleaned_data["visual"]
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(URL)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(URL)


@login_required(login_url="profile:login")
def likeproduct(request, id):
    URL = request.META.get("HTTP_REFERER")  # get last url
    current_user = request.user  # access user session information
    product_like = LikedList.objects.filter(product_id=id, user_id=current_user.id)

    if not product_like:
        data = LikedList()
        data.user_id = current_user.id
        data.product_id = id
        data.save()
        messages.success(request, "Product added to Which List")
        return HttpResponseRedirect(URL)

    return HttpResponseRedirect(URL)


def addtoshopcart_old(request, id):
    URL = request.META.get("HTTP_REFERER")  # get last url
    current_user = request.user  # access user session information
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1  # the product is in the cart
    else:
        control = 0  # the product is not in cart

    if request.method == "POST":  # (detail page)
        colors_id = request.POST.get("colors")
        materiel_id = request.POST.get("materiels")
        demension_id = request.POST.get("demension")
        variant = Variants.objects.filter(
            product_id=id,
            color_id=colors_id,
            demension_id=demension_id,
            materiel_id=materiel_id,
        )
        print(f"##### variants ###{variant}")
        return HttpResponseRedirect(URL)

    else:  # there is no post (Home page)
        if control == 1:  # update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.user_id = current_user.id
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(URL)
