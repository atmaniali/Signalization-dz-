from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Q
import os
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from home.models import Settings
from order.models import ShopCart
from product.models import Category, Images, Product, Variants, Visuel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from user.models import UserProfile

# Create your views here.


def index(request):
    template_name = "product/index.html"
    category = request.GET.get("category")
    color = request.GET.get("color")
    demension = request.GET.get("demension")
    materiel = request.GET.get("materiel")
    cat_set = Category.objects.filter(parent=None)
    # filter by category
    if category:
        category_id = force_str(urlsafe_base64_decode(category))
        products_list = Product.objects.filter(category_id=category_id)
    # filter by color
    elif color:
        color_id = force_str(urlsafe_base64_decode(color))
        variant_list = Variants.objects.filter(color_id=color_id).values_list(
            "product_id"
        )
        products_list = Product.objects.filter(id__in=variant_list)
    # filter by demension
    elif demension:
        demension_id = force_str(urlsafe_base64_decode(demension))
        variant_list = Variants.objects.filter(demension_id=demension_id).values_list(
            "product_id"
        )
        products_list = Product.objects.filter(id__in=variant_list)
    # filter by materiel
    elif materiel:
        materiel_id = force_str(urlsafe_base64_decode(materiel))
        variant_list = Variants.objects.filter(materiel_id=materiel_id).values_list(
            "product_id"
        )
        products_list = Product.objects.filter(id__in=variant_list)
    else:
        products_list = Product.objects.all()
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    products_category = Product.objects.raw(
        "SELECT 1 AS id, category_id , count(id) FROM product_product GROUP BY category_id "
    )

    product_color = Variants.objects.raw(
        "SELECT 1 AS id,color_id, count(id) FROM product_variants GROUP BY color_id"
    )

    # product_demension = Variants.objects.raw(
    #     "SELECT * FROM product_variants GROUP BY demension_id")
    product_demension = Variants.objects.raw(
        "SELECT 1 AS id,demension_id, count(id) FROM product_variants GROUP BY demension_id"
    )
    # print(f")))))) {product_demension}")

    product_materiels = Variants.objects.raw(
        "SELECT 1 AS id,materiel_id, count(id) FROM product_variants GROUP BY materiel_id"
    )

    paginator = Paginator(products_list, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        # 'cat_set': cat_set,
        "setting": setting,
        "category_filter": category_filter,
        "page_obj": page_obj,
        "products_category": products_category,
        "product_color": product_color,
        "product_demension": product_demension,
        "product_materiels": product_materiels,
        # 'product_visuels': product_visuels,
    }
    # add number of product in cart and amount and list cart
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)


def subcategory(request, slug_cat):
    template_name = "product/subcategory_list.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    cat = get_object_or_404(Category, slug=slug_cat)
    category = Category.objects.filter(parent=cat.id)
    count = Product.objects.filter(category=cat.id).count()  # number of products
    category_ancestors = cat.get_ancestors()  # all parrents of category
    categors_is_leaf = cat.is_leaf_node()  # category is node
    products = Product.objects.filter(category=cat.id)
    paginator = Paginator(products, 20)  # pagination
    page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "setting": setting,
        "category": category,
        "cat": cat,
        # 'cat_set': cat_set,
        "category_ancestors": category_ancestors,
        "category_filter": category_filter,
        "categors_is_leaf": categors_is_leaf,
        "products": products,
        "count": count,
    }
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    return render(request, template_name, context)


def product_detail(request, id, product_slug):
    template_name = "product/detail.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    product_id = force_str(urlsafe_base64_decode(id))
    product = get_object_or_404(Product, slug=product_slug, id=product_id)
    visuels = product.product_productvisual.all()
    product.product_views += 1
    product.save()
    product_similer = Product.objects.filter(
        Q(category_id=product.category.id), ~Q(id=product.id)
    )[0:4]
    cat = get_object_or_404(Category, id=product.category.id)
    images = Images.objects.filter(product_id=product_id)
    category_ancestors = cat.get_ancestors(include_self=True)
    query = request.GET.get("q")
    cat_set = Category.objects.filter(parent=None)

    # return HttpResponse(f'{cat}')
    context = {
        "category_filter": category_filter,
        "setting": setting,
        "product": product,
        # 'cat_set': cat_set,
        "category_ancestors": category_ancestors,
        "images": images,
        "product_similer": product_similer,
        "visuels": visuels,
    }
    # add number of product in cart and amount and list cart
    current_user = request.user.id
    if current_user:
        userprofile = UserProfile.objects.get(
            user_id=current_user
        )  # to add information about cart
        shopcarts = ShopCart.objects.filter(user_id=current_user)
        context.update({"shopcarts": shopcarts, "userprofile": userprofile})
    if product.variant != None:
        variants = Variants.objects.filter(product_id=product_id)
        # variant = Variants.objects.get(id=variants[0].id)
        demensions = Variants.objects.raw(
            "SELECT 1 AS id,demension_id, count(id) FROM product_variants WHERE product_id=%s GROUP BY demension_id",
            [product_id],
        )
        colors = Variants.objects.raw(
            "SELECT 1 AS id,color_id, count(id) FROM product_variants WHERE product_id=%s GROUP BY color_id",
            [product_id],
        )
        # colors = [x for x in colors_set]
        materiels = Variants.objects.raw(
            "SELECT 1 AS id,materiel_id FROM product_variants WHERE product_id=%s GROUP BY materiel_id",
            [product_id],
        )
        types = Variants.objects.raw(
            "SELECT 1 AS id,type_id FROM product_variants WHERE product_id=%s GROUP BY type_id",
            [product_id],
        )
        fasteners = Variants.objects.raw(
            "SELECT 1 AS id,fastner_id FROM product_variants WHERE product_id=%s GROUP BY fastner_id",
            [product_id],
        )
        # visuels = Variants.objects.raw(
        #     "SELECT 1 AS id,visuel_id FROM product_variants WHERE product_id=%s GROUP BY visuel_id", [product_id])
        typologies = Variants.objects.raw(
            "SELECT 1 AS id,typologie_id FROM product_variants WHERE product_id=%s GROUP BY typologie_id",
            [product_id],
        )
        adehesives = Variants.objects.raw(
            "SELECT 1 AS id,adehesive_id FROM product_variants WHERE product_id=%s GROUP BY adehesive_id",
            [product_id],
        )

        context.update(
            {
                #     # 'variant': variant,
                "demensions": demensions,
                "colors": colors,
                "materiels": materiels,
                "types": types,
                "fasteners": fasteners,
                # 'visuels': visuels,
                "typologies": typologies,
                "adehesives": adehesives,
            }
        )
    # TODO create separate function, change debug mode in prod

    return render(request, template_name, context)


def ajaxPrice(request):
    data = {}
    if request.method == "GET":
        print("get")
        print(request)
        productid = request.GET["productid"]
        materielid = request.GET["materialid"]
        demensionid = request.GET["demensionid"]
        # visuelid = request.GET['visuelid']
        typologieid = request.GET["typologieid"]
        colorid = request.GET["colorid"]
        fastnerid = request.GET["fastnerid"]
        typeid = request.GET["typeid"]
        typologieid = request.GET["typologieid"]
        adehesiveid = request.GET["adehesiveid"]
        # productid=5&materialid=5&demensionid=4&visuelid=6
        print(f"PRODUCTID {request.GET}")

        if demensionid and colorid and adehesiveid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    color_id=colorid,
                    adehesive_id=adehesiveid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif demensionid and materielid and typeid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    materiel_id=materielid,
                    type_id=typeid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif colorid and typeid and adehesiveid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    color_id=colorid,
                    type_id=typeid,
                    adehesive_id=adehesiveid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif colorid and typeid and fastnerid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    color_id=colorid,
                    type_id=typeid,
                    fastner_id=fastnerid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif demensionid and adehesiveid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    adehesive_id=adehesiveid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif materielid and colorid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, color_id=colorid, materiel_id=materielid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif demensionid and materielid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    materiel_id=materielid,
                )
                print(f"TRY | {variant} |{variant.id} | {variant.price}")
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()
                print(f"CATCH | {variant} |{variant.id} | {variant.price}")

        elif demensionid and materielid and colorid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    color_id=colorid,
                    materiel_id=materielid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        # elif visuelid and adehesiveid:
        #     try:
        #         variant = Variants.objects.get(
        #             product_id=productid, visuel_id=visuelid, adehesive_id=adehesiveid)
        #     except ObjectDoesNotExist:
        #         variant = Variants.objects.filter(id=productid).first()

        elif demensionid and materielid:
            try:
                variant = Variants.objects.get(
                    product_id=productid,
                    demension_id=demensionid,
                    materiel_id=materielid,
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif typologieid and colorid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, typologie_id=typologieid, color_id=colorid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif colorid and fastnerid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, fastner_id=fastnerid, color_id=colorid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif adehesiveid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, adehesive_id=adehesiveid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif typologieid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, typologie_id=typologieid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        # elif visuelid:
        #     try:
        #         variant = Variants.objects.get(
        #             product_id=productid, visuel_id=visuelid)
        #     except ObjectDoesNotExist:
        #         variant = Variants.objects.filter(id=productid).first()

        elif fastnerid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, fastner_id=fastnerid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif typeid:
            try:
                variant = Variants.objects.get(product_id=productid, type_id=typeid)
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif colorid:
            try:
                variant = Variants.objects.get(product_id=productid, color_id=colorid)
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif materielid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, materiel_id=materielid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()

        elif demensionid:
            try:
                variant = Variants.objects.get(
                    product_id=productid, demension_id=demensionid
                )
            except ObjectDoesNotExist:
                variant = Variants.objects.filter(id=productid).first()
        else:
            variant = Variants.objects.filter(product_id=productid).first()

        data = {
            "test": "success test",
            "productid": productid,
            "materielid": materielid,
            "demensionid": demensionid,
            # 'visuelid': visuelid,
            "price": variant.price,
        }
        # productid=5&materialid=6&demensionid=3&visuelid=5&typologieid=&colorid=&fastnerid=&typeid=&adehesiveid=
        # productid=5&materialid=1&demensionid=1&visuelid=19&typologieid=&colorid=&fastnerid=&typeid=&adehesiveid=
        return JsonResponse(data)
    return JsonResponse(data)


def product_change(request):
    template_name = "product/change.html"
    category_filter = Category.objects.all()  # filter and search in head.html
    setting = Settings.objects.get(id=1)  # information global of site
    product = Product.objects.get(id=10)
    images = Images.objects.filter(product_id=10)
    cat_set = Category.objects.filter(parent=None)
    context = {
        "category_filter": category_filter,
        "setting": setting,
        "product": product,
        "images": images,
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


def dawnload_pdf(request, id):
    document = get_object_or_404(Product, pk=id)
    print(f"DOCUMENT : {document}")
    print(f"DOCUMENT PDF : {document.fiche}")
    response = HttpResponse(document.fiche, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{document.fiche.name}"'
    return response
