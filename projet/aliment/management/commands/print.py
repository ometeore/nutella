from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, DataError
from aliment.models import Aliment, Categorie
import django.core.exceptions
import requests




def get_list_aliment(categorie, nbr_elm):
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
    return encoded["products"]

class Command(BaseCommand):

    def handle(self, *args, **options):

        products = get_list_aliment("nutella",10)

        ##### Pour chacun des aliments on crée une instance et on le sauvgarde
        for product in products:

            alm, ack = Aliment.objects.get_or_create(nom=product["product_name_fr"])
            alm.note_nutritionelle = product["nutrition_grades_tags"][0]

            try:
                alm.url_off = product["url"]
                alm.url_img = product["image_url"]
                alm.glucide_100g = product["nutriments"]["carbohydrates_100g"]
                alm.sugar_100g = product["nutriments"]["sugars_100g"]
                alm.salt_100g = product["nutriments"]["salt_100g"]
                alm.acide_100g = product["nutriments"]["saturated-fat_100g"]
                str_all_categories = product["categories"]
            except KeyError as e:
                print("bug")
                print(e)
                continue


            ##### Pour les catégories On balaye le champs catégories et on ajoute si on ne l'a pas encore en base
            
            list_all_categories = str_all_categories.split(",")
            for cat_of_elm2 in list_all_categories[0:3]:

                ##### On verifie si il existe en base si oui on l'ajoute dans les cat de l'aliment si non
                cat_of_elm = cat_of_elm2.strip()
                try:
                    cat_already_exist = Categorie.objects.get(nom=cat_of_elm)
                    alm.categorie.add(cat_already_exist)

                except Categorie.DoesNotExist:
                    new_cat = Categorie()
                    new_cat.nom = cat_of_elm
                    new_cat.save()
                    alm.categorie.add(new_cat)

            ### sauvegarde de l'aliment ssi complet
            try:
                alm.save()
            except Aliment.DataError:
                print("oups, fail\n")

