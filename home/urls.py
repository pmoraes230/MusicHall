from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    # USERS
    path("list_user/", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:user_id>/", views.update_user, name="update_user"),
    
    # EVENT
    path("deteils_event/<int:id_event>/", views.details_event, name="deteils_event")
]
