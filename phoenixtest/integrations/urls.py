from django.urls import path

from . import views

urlpatterns = [
    path("qwe", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("integration", views.get_users, name="get_users")
]