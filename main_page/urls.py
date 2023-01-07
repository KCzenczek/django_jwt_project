from django.urls import path

from main_page import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("login", views.f_login, name="f_login"),
    path("logout", views.f_logout, name="f_logout"),

]
