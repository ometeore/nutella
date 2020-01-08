from django.urls import path
from aliment.views import aliment, v_accueil, recherche

app_name = "aliment"


urlpatterns = [
    path("recherche", recherche.index, name="recherche"),
    path("", aliment.index, name="index"),
    path("<int:aliment_id>/", aliment.detail, name="detail"),
    path("substitute/<int:aliment_id>/", aliment.substitute, name="substitute"),
    path("delete/<int:aliment_id>/", aliment.delete_aliment_of_user, name="delete"),
]
