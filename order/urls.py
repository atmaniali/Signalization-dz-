from . import views
from django.urls import path

app_name = "order"
urlpatterns = [
    path("", views.shopcart, name="shopcart"),
    path("addtoshopcart/<int:id>", views.addtoshopcart, name="addtoshopcart"),
    path("shopcartdetail/<str:id>", views.shopcartdetail, name="shopcartdetail"),
    path("deletefromcart/<str:id>", views.deletefromcart, name="deletefromcart"),
    path("orderproduct/", views.orderproduct, name="orderproduct"),
    # path('orderproduct/', views.orderproduct, name='orderproduct'),
    path("likeproduct/<int:id>", views.likeproduct, name="likeproduct"),
]
