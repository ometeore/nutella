from django.conf import settings
from django.contrib import admin
from django.urls import path
from espace_admin import views

app_name = "espace_admin"

urlpatterns = [
    path("", views.manage_cat, name="manage_cat"),
    path("selection/", views.categorie_search, name='selection'),
    path("old/", views.index, name="index"),
    path("old/add/", views.add_cat, name="add_cat"),
]