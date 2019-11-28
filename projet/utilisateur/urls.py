from django.urls import path
from utilisateur import views

app_name = "user"


urlpatterns = [
    path("", views.connexion, name="connexion"),
    path("profil", views.mon_compte, name="profil_user"),
    path("create", views.create, name="inscription"),
    path("deconnexion", views.deconnexion, name="deconnexion"),
]
