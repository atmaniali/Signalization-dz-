from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from home import views as myviews


admin.site.site_header = "Moumen Panel"
urlpatterns = [
    # path("", include("admin_soft.urls")),
    path("admin/", include("admin_honeypot.urls")),
    path("moumen-admin/", admin.site.urls),
    path("", include("home.urls")),
    path("product/", include("product.urls")),
    path("user/", include("user.urls")),
    path("order/", include("order.urls")),
    # 3rd party link
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("check-seo/", include("django_check_seo.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = myviews.error_404
handler500 = myviews.error_500
