from . import views
from django.urls import path


app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    # TODO : search auto doesn't work
    path("search_auto/", views.search_auto, name="search_auto"),
    path("contactus/", views.contactus, name="contactus"),
    path("faq/", views.faq, name="faq"),
    path("rating/", views.rating, name="rating"),
    path("addReview/", views.addReview, name="addrating"),
    path("about/", views.aboutus, name="aboutus"),
]
