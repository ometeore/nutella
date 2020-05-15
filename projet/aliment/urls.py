from django.urls import path
from aliment.views import aliment, v_accueil, recherche
from django.urls import path
app_name = "aliment"


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("recherche", recherche.index, name="recherche"),
    path("validation", recherche.validate_search, name='validation'),
    path("", aliment.index, name="index"),
    path("<int:aliment_id>/", aliment.detail, name="detail"),
    path("substitute/<int:aliment_id>/", aliment.substitute, name="substitute"),
    path("delete/<int:aliment_id>/", aliment.delete_aliment_of_user, name="delete"),
    path('sentry-debug', trigger_error, name="sentry test"),
]
