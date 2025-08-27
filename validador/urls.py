from django.urls import path
from . import views

urlpatterns = [
    path("validador", views.validation, name="validador")
]
