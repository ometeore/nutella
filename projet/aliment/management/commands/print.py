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
        incomplete = 0
        name_too_long = 0
        api = 0
        save = 0
        names = []
        list_of_categorie = ["viande","biscuit","legume","snacks","Boissons","Produits laitiers","Céréales et pommes de terre"]
        list_of_categorie = ["Produits fermentés","Produits à tartiner","Biscuits et gâteaux","Charcuteries","Fromages","Desserts"  ]
        list_of_categorie = ["Sauces", "Produits de la mer", "Surgelés", "Confiseries", "Conserves", "Poissons", "Boissons alcoolisées", "Biscuits", "Boissons aux fruits", "Chocolats", "Matières grasses", "Condiments", "Jus et nectars", "Produits déshydratés", "Pains", "Confitures", "Jus de fruits", "Boissons chaudes", "Vins", "Graines", "Produits de la ruche", "Desserts lactés"]
        list_of_categorie = ["Produits de la ruche"]
        for cat in list_of_categorie:
            products = get_list_aliment(cat,400)

            ##### Pour chacun des aliments on crée une instance et on le sauvgarde
            for product in products:
                if not product.get("product_name_fr"):
                    continue
                if Aliment.objects.filter(nom=product["product_name_fr"]).count():
                    continue

                try:
                    alm = Aliment(nom=product["product_name_fr"])
                except (KeyError, DataError) as f:
                    name_too_long = name_too_long + 1
                    print("name too long")
                    print(f)
                    continue
                try:
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
                except KeyError as e:
                    print("api does not respond")
                    api = api + 1
                    print(e)
                    continue
                
                
                ### sauvegarde de l'aliment ssi complet
                try:
                    alm.save()
                    names.append(alm.nom)
                    save = save + 1
                except DataError as e:
                    incomplete = incomplete + 1
                    print("aliment incomplete")
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
                        new_DataErrorcat.save()
                        alm.categorie.add(new_cat)


        print("les aliments qu'on a éssayer de sauvegarder incomlet")
        print(incomplete)
        print("les aliments dont le nom est trop long")
        print(name_too_long)
        print("l'api n'a pas la categorie recherchée")
        print(api)
        print("les aliments sauvegardés")
        print(save)
        print("le nom des aliments sauvegardés")
        print(names)


