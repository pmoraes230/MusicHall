from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:user_id>/", views.update_user, name="update_user")
]
