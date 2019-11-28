from django.core.management.base import BaseCommand, CommandError
from aliment.models import Aliment, Categorie
import django.core.exceptions
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):

        ##### On selectionne la categorie sous format texte
        categorie = "Fruits tropicaux"
        nbr_elm = 25

        # a eu acces aux images en etant hors connexion?????

        ##### Fait bosser l'API retourne dans products un json contenant des aliments
        url_new = "https://fr.openfoodfacts.org/cgi/search.pl"
        getVars = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": categorie,
            "sort_by": "unique_scans_n",
            "page_size": nbr_elm,
            "axis_x": "energy",
            "axis_y": "products_n",
            "json": '1',
        }

        encoded = requests.get(url_new, params=getVars).json()
        products = encoded["products"]  # <-- list

        ##### Pour chacun des aliments on crée une instance et on le sauvgarde
        for product in products:

            alm, ack = Aliment.objects.get_or_create(nom=product["product_name_fr"])

            alm.note_nutritionelle = product["nutrition_grades_tags"][0]
            
            alm.url_off = product["url"]
            alm.url_img = product["image_url"]

            ##### Pour les catégories On balaye le champs catégories et on ajoute si on ne l'a pas encore en base
            str_all_categories = product["categories"]
            list_all_categories = str_all_categories.split(",")
            for cat_of_elm2 in list_all_categories[0:3]:

                ##### On verifie si il existe en base si oui on l'ajoute dans les cat de l'aliment si non
                cat_of_elm = cat_of_elm2.strip()
                try:
                    cat_already_exist = Categorie.objects.get(nom=cat_of_elm)
                    alm.save()
                    alm.categorie.add(cat_already_exist)

                except Categorie.DoesNotExist:
                    new_cat = Categorie()
                    new_cat.nom = cat_of_elm
                    new_cat.save()
                    alm.save()
                    alm.categorie.add(new_cat)
