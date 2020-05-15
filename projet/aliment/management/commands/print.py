from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, DataError
from aliment.models import Aliment, Categorie
from django.conf import settings
import django.core.exceptions
import requests
import json




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
    try:
        encoded = requests.get(url_new, params=getVars).json()
        return encoded["products"]
    except(KeyError, IndexError):
        return None
    return encoded["products"]


####    On lui envoi un json extrait de l'API il retourne True pour dire pret a être sauvegardé ou False pour 
#    lui dire que l'élément est corrompue

def aliment_test(product):

    if not product.get("product_name_fr"):
        return False
    if Aliment.objects.filter(nom=product["product_name_fr"]).count():
        return False

    try:
        alm = Aliment(nom=product["product_name_fr"])
    except (KeyError, DataError) as f:
        return False
    try:
        alm.note_nutritionelle = product["nutrition_grades_tags"][0]
        alm.glucide_100g = product["nutriments"]["carbohydrates_100g"]
        alm.sugar_100g = product["nutriments"]["sugars_100g"]
        alm.salt_100g = product["nutriments"]["salt_100g"]
        alm.acide_100g = product["nutriments"]["saturated-fat_100g"]
        str_all_categories = product["categories"]
        alm.url_off = product["url"]
        if product["image_url"] == '':
            alm.url_img = None
        else:
            alm.url_img = product["image_url"]

    except KeyError as e:
        return False
    try:
        return True
    except DataError as e:
        return False
    else:
        return False


def insert_categorie(list_all_categories, alm):
    for cat_of_elm2 in list_all_categories:

        ##### On verifie si il existe en base si oui on l'ajoute dans les cat de l'aliment si non
        cat_of_elm = cat_of_elm2.strip()
        try:
            cat_already_exist = Categorie.objects.get(nom=cat_of_elm)
            alm.categorie.add(cat_already_exist)

        except Categorie.DoesNotExist:
            new_cat = Categorie(nom=cat_of_elm)
            new_cat.save()
            alm.categorie.add(new_cat)



#### sauvegarde un aliment renvoi l'ensemble des catégories à lui associer
def go_save(product):
    alm = Aliment(nom=product["product_name_fr"])
    alm.note_nutritionelle = product["nutrition_grades_tags"][0]
    alm.url_off = product["url"]
    if product["image_url"] == '':
        alm.url_img = None
    else:
        alm.url_img = product["image_url"]
        alm.glucide_100g = product["nutriments"]["carbohydrates_100g"]
        alm.sugar_100g = product["nutriments"]["sugars_100g"]
        alm.salt_100g = product["nutriments"]["salt_100g"]
        alm.acide_100g = product["nutriments"]["saturated-fat_100g"]
        str_all_categories = product["categories"]
    alm.save()
    list_all_categories = str_all_categories.split(",")
    insert_categorie(list_all_categories, alm)





class Command(BaseCommand):
    def handle(self, *args, **options):
        list_of_categorie = ["Produits de la ruche"]
        list_of_categorie = list_of_categorie + ["viande","biscuit","legume","snacks","Boissons","Produits laitiers","Céréales et pommes de terre"]
        #list_of_categorie = list_of_categorie + ["Produits fermentés","Produits à tartiner","Biscuits et gâteaux","Charcuteries","Fromages","Desserts"  ]
        #list_of_categorie = list_of_categorie + ["Sauces", "Produits de la mer", "Surgelés", "Confiseries", "Conserves", "Poissons", "Boissons alcoolisées", "Biscuits", "Boissons aux fruits", "Chocolats", "Matières grasses", "Condiments", "Jus et nectars", "Produits déshydratés", "Pains", "Confitures", "Jus de fruits", "Boissons chaudes", "Vins", "Graines", "Produits de la ruche", "Desserts lactés"]
        
        success = 0
        fail = 0
        for cat in list_of_categorie:
            products = get_list_aliment(cat, settings.NOMBRE_A_IMPORTER)

            ##### Pour chacun des aliments on crée une instance et on le sauvegarde
            for product in products:    
                product_test = aliment_test(product)
                if product_test:
                    try:
                        success = success + 1
                        go_save(product)
                    except:
                        fail = fail + 1
                        continue

                else:
                    fail = fail + 1
                    continue


            print('\n\n')
            print("reussi: {}\n".format(success))
            print("échoué: {}\n".format(fail))