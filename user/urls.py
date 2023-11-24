from . import views
from django.urls import path

app_name = "profile"
urlpatterns = [
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("", views.index, name="profile"),
    path("update/", views.user_update, name="user_update"),
    path("orders/", views.user_order, name="user_order"),
    path("favorit/", views.user_likedproduct, name="user_likedproduct"),
    path("favorit/delete/<str:id>/", views.delete_favorit, name="delete_favorit"),
    path("orderdetail/<str:id>", views.user_order_detail, name="user_order_detail"),
    path("orders_product/", views.user_order_product, name="user_order_product"),
    path(
        "order_product_detail/<str:id>/<str:oid>",
        views.user_order_product_detail,
        name="user_order_product_detail",
    ),
    # change password user login
    path("password/", views.user_password, name="user_password"),
    # change password ! login
    path("reset/", views.reset_password, name="reset_password"),
    path("done/", views.email_sent_done, name="email_sent_done"),
    path("<uidb64>/<token>/", views.change_password, name="user_reset_password"),
    path("test/", views.test_mail_template, name="test")
    # TODO crypte and decrypte every url with {id} in parametre
]
