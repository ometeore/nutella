import datetime
from django.db import models
from django.utils import timezone


class Aliment(models.Model):
    nom = models.CharField("nom", max_length=50)
    note_nutritionelle = models.CharField(max_length=1)
    categorie = models.ManyToManyField("aliment.Categorie")
    url_off = models.CharField(max_length=150)
    url_img = models.CharField(max_length=150)
    glucide_100g = models.DecimalField(max_digits=8, decimal_places=4)
    sugar_100g = models.DecimalField(max_digits=8, decimal_places=4)
    salt_100g = models.DecimalField(max_digits=8, decimal_places=4)
    acide_100g = models.DecimalField(max_digits=8, decimal_places=4)


    def __str__(self):
        return self.nom

    def substitute(self):
        pass


class Categorie(models.Model):
    nom = models.CharField("nom", max_length=80, unique=True)  # NOT NULL

    def __str__(self):
        return self.nom
