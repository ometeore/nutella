from django.urls import path
from aliment.views import views, v_accueil, recherche

app_name = "aliment"


urlpatterns = [
    path("recherche", recherche.index, name="recherche"),
    path("", views.index, name="index"),
    path("<int:aliment_id>/", views.detail, name="detail"),
    path("substitute/<int:aliment_id>/", views.substitute, name="substitute"),
    path("delete/<int:aliment_id>/", views.delete_aliment_of_user, name="delete"),
]
