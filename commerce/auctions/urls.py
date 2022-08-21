from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listing/<int:idl>", views.listingPage, name="listingPage"),
    path("watchList", views.watchListPage, name="watchPage"),
    path("all", views.all, name='all'),
    path("catagories", views.catagories, name="catagories"),
    path("catagory/<str:catagory>", views.catagory, name='catagory')
]
