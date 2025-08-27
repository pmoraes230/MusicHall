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
    path("delete_user/<id_user>/", views.delete_user, name="delete_user"),
    
    # EVENT
    path("deteils_event/<int:id_event>/", views.details_event, name="deteils_event"),
    path("buy_ticket/<int:id_event>/", views.buy_ticket, name="buy_client"),
    path("list_tickets/<int:id_event>/", views.list_tickets, name="list_tickets"),
    path("update_event/<int:id_event>/", views.update_event, name="update_event"),
    path("delete_event/<int:id_event>/", views.delete_event, name="delete_event"),
    path("register_event/", views.register_event, name="register_event"),
    path("register_client/<int:id_event>/", views.register_client, name="register_client"),
    path("ticket_generate/<str:id_ticket>/", views.generate_ticket, name="ticket_generate"),
    path("tickets_download/", views.tickets_download, name="tickets_download"),
    
    # SECTOR
    path("list_sector/<int:id_event>/", views.list_sector, name="list_sector"),
    path("register_sector/<int:id_event>/", views.register_sector, name="register_sector"),
    path("update_sector/<int:id_sector>/", views.update_sector, name="update_sector"),
    path("delete_sector/<int:id_sector>/", views.delete_sector, name="delete_sector"),
]
