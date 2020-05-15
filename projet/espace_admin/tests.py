from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase, Client
from aliment.models import Aliment, Categorie
from utilisateur.models import MyUser
from django.db import transaction
import pytest
import requests


class TestAliment(TestCase):
    def setUp(self):
        cat1 = Categorie.objects.create(nom="Fruit", insert=False)
        cat2 = Categorie.objects.create(nom="Steak", insert=True)

        # la bannane a plus de glucide que la pomme
        self.Banane = Aliment.objects.create(nom="Banane",note_nutritionelle="a", url_off="http",url_img="http2", glucide_100g="12",salt_100g="1", sugar_100g="1", acide_100g="1")
        self.Banane.categorie.add(cat1)
        self.Pomme = Aliment.objects.create(nom="Pomme",note_nutritionelle="a", url_off="http",url_img="http2", glucide_100g="1",salt_100g="1", sugar_100g="1", acide_100g="1")
        self.Pomme.categorie.add(cat1)
        self.Poire = Aliment.objects.create(nom="Poire",note_nutritionelle="b", url_off="http",url_img="http2", glucide_100g="0.123",salt_100g="0.123", sugar_100g="0.123", acide_100g="0.123")
        self.Poire.categorie.add(cat1)
        self.Tournedos = Aliment.objects.create(nom="Tournedos",note_nutritionelle="c", url_off="http",url_img="http2", glucide_100g="0.123",salt_100g="0.123", sugar_100g="0.123", acide_100g="0.123")
        self.Tournedos.categorie.add(cat2)
        self.prods =[
            {
                "product_name_fr": "patate",
                "nutrition_grades_tags": [
                    "b"
                ],
                "url": "https://fr.openfoodfacts.org/produit/8000500310427/nutella-biscuits",
                "image_url": "https://static.openfoodfacts.org/images/products/309/575/769/7105/front_fr.94.400.jpg",
                "nutriments": {
                    "carbohydrates_100g": 0.9,
                    "sugars_100g": 0.9,
                    "salt_100g": 1.4,
                    "saturated-fat_100g": 0.5,
                },
                "categories": "Produits à tartiner,Viandes,Produits à tartiner salés,Charcuteries,Rillettes,Rillettes de viande,Rillettes de viande blanche,Rillettes de volaille,Rillettes de poulet",
            },
            {
                "product_name_fr": "patate2",
                "nutrition_grades_tags": [
                    "b"
                ],
                "url": "https://fr.openfoodfacts.org/produit/8000500310427/nutella-biscuits",
                "image_url": "https://static.openfoodfacts.org/images/products/309/575/769/7105/front_fr.94.400.jpg",
                "nutriments": {
                    "carbohydrates_100g": 0.9,
                    "sugars_100g": 0.9,
                    "salt_100g": 1.4,
                    "saturated-fat_100g": 0.5,
                },
                "categories": "Produits à tartiner,Viandes,Produits à tartiner salés,Charcuteries,Rillettes,Rillettes de viande,Rillettes de viande blanche,Rillettes de volaille,Rillettes de poulet",
            },
            {
                "product_name_fr": "patate_incomplete",
                "url": "https://fr.openfoodfacts.org/produit/8000500310427/nutella-biscuits",
                "image_url": "https://static.openfoodfacts.org/images/products/309/575/769/7105/front_fr.94.400.jpg",
                "nutriments": {
                    "carbohydrates_100g": 0.9,
                    "sugars_100g": 0.9,
                    "salt_100g": 1.4,
                    "saturated-fat_100g": 0.5,
                },
                "categories": "Produits à tartiner,Viandes,Produits à tartiner salés,Charcuteries,Rillettes,Rillettes de viande,Rillettes de viande blanche,Rillettes de volaille,Rillettes de poulet",
            }
        ]


    def test_page_return_200(self):
        ### Test qu'on a bien une reponse en demandant l'accueil ###
        c = Client()
        cat1 = Categorie.objects.get(nom="Fruit")
        cat2 = Categorie.objects.get(nom="Steak")
        response = c.get('/espace_admin/')
        response2 = c.post('/espace_admin/add', {'cat': [cat1.pk], 'nombre': 21, 'datatable_categorie_length' : 10})
        self.assertEqual(response.status_code, 200)

    def test_aliment_test(self):
        cat1 = Categorie.objects.get(nom="Fruit")
        self.assertEqual(cat1.aliment_test(self.prods[0]), True)
        self.assertEqual(cat1.aliment_test(self.prods[2]), False)

    #tester nombre se fait depuis le formulaire je ne vois pas de cas ou ca retournerai errors....
    def test_import_cat(self):
        cat1 = Categorie.objects.get(nom="Fruit")
        cat2 = Categorie.objects.get(nom="Steak")
        self.assertEqual(cat2.import_cat(), -1)
    

    @patch.object(Categorie, 'get_list_aliment')
    def test_get_list_aliment(self, mock_function):
        mock_function.return_value = self.prods
        cat1 = Categorie.objects.get(nom="Fruit")
        result = cat1.get_list_aliment()
        self.assertEqual(result[0]['product_name_fr'], "patate")

    @patch.object(Categorie, 'get_list_aliment')
    def test_import_cat1(self, mock_function):
        mock_function.return_value = self.prods
        cat1 = Categorie.objects.get(nom="Fruit")
        result = cat1.import_cat()
        self.assertEqual(result, 2)