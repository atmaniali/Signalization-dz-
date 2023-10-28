from . import views
from django.urls import path

app_name = "product"
urlpatterns = [
    path("", views.index, name="index"),  # list of product
    path("ajaxPrice/", views.ajaxPrice, name="ajaxPrice"),  # list of product
    path("product_change/", views.product_change, name="product_change"),
    path("dawnload_pdf/<int:id>/", views.dawnload_pdf, name="dawnload_pdf"),
    path(
        "<str:id>/<str:product_slug>/", views.product_detail, name="product_detail"
    ),  # product detail
    path(
        "<str:slug_cat>/", views.subcategory, name="subcategory"
    ),  # all child of category
]
