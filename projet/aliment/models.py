from django.db import models
from django.conf import settings
import requests



def compare_list(list1, list2):
    number_of_common_value = 0 
    for i in range(0, len(list1)):
        if list1[i] in list2[0:len(list2)]:
            number_of_common_value += 1 
    return number_of_common_value



class Aliment(models.Model): 
    nom = models.CharField("nom", max_length=50)
    note_nutritionelle = models.CharField(max_length=1)
    categorie = models.ManyToManyField("aliment.Categorie")
    url_off = models.CharField(max_length=150)
    url_img = models.CharField(max_length=150)
    glucide_100g = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    sugar_100g = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    salt_100g = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    acide_100g = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)


    def __str__(self):
        return self.nom

    def sum_nutrition(self):
        if(isinstance(self.salt_100g, int) or isinstance(self.acide_100g, int) or isinstance(self.sugar_100g, int) or isinstance(self.glucide_100g, int)):
            return self.salt_100g + self.acide_100g + self.sugar_100g + self.glucide_100g
        else:
            return 100
    
    def is_complete(self):
    ###      test que doit remplir un aliment avant d'être sauvegarder #####
        if self.nom != "":
            if self.note_nutritionelle in ["a","b","c","d","e"]:
                return True
        return False

    def substitute(self):
        ### retourne une liste de 6 objets aliment de meilleurs qualités nutritionnels ###
        ### cad : aliment avec en priorité un maximum de categorie en commun 
        ###       obligatoirement avec une meilleur note nutritionelle
        ###       trié par la somme des reperes nutritionel

        cat = list(self.categorie.values_list("pk", flat=True))
        aliments_same_categorie = list(Aliment.objects.filter(categorie__pk__in=cat).order_by('note_nutritionelle') )
        aliments_same_categorie = [aliment for aliment in aliments_same_categorie if aliment.nom != self.nom]
        
        need_to_keep_looking = True
        final_list = []
        candidates = []
        common_cat_numbers = 3

        while need_to_keep_looking:
            for al in aliments_same_categorie:
                cats_of_potential_substitute = list(al.categorie.values_list("pk", flat="True"))
                if(compare_list(cats_of_potential_substitute, cat) == common_cat_numbers):
                    if(al.note_nutritionelle <= self.note_nutritionelle):
                        if al in candidates:
                            pass
                        else:
                            candidates.append(al)
            if len(candidates) < 6:
                common_cat_numbers = common_cat_numbers - 1
                if common_cat_numbers == 0:
                    need_to_keep_looking = False
            else:
                need_to_keep_looking = False

        final_list = sorted(candidates, key=lambda aliment: aliment.sum_nutrition(), reverse=False)
        print(final_list)
        return final_list[0:6]






########################################################### CATEGORIES

class Categorie(models.Model):
    nom = models.CharField("nom", max_length=80, unique=True)
    insert = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def import_cat(self):
        success = 0
        if self.insert == True:
            return -1
        else:
            products = self.get_list_aliment()
            ##### Pour chacun des aliments on crée une instance et on le sauvegarde
            for product in products:    
                product_test = self.aliment_test(product)
                if product_test:
                    try:
                        success = success + 1
                        self.go_save(product)
                    except:
                        continue

                else:
                    continue
        return success



    def get_list_aliment(self):
    ### Appele l'API d'open food fact retourne sous forme de json une liste de produits appartenant a la categorie  

        url_new = "https://fr.openfoodfacts.org/cgi/search.pl"
        getVars = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": self.nom,
            "sort_by": "unique_scans_n",
            "page_size": settings.NOMBRE_A_IMPORTER,
            "axis_x": "energy",
            "axis_y": "products_n",
            "json": '1',
        }
        try:
            encoded = requests.get(url_new, params=getVars).json()
            print(encoded['products'])
            return encoded["products"]
        except(KeyError, IndexError):
            return None
        return encoded["products"]


    def aliment_test(self, product):

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

    #### sauvegarde un aliment renvoi l'ensemble des catégories à lui associer
    def go_save(self, product):
        nbr_alm = 0
        nbr_cat = 0
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
        for cat_of_elm2 in list_all_categories:

            ##### On verifie si il existe en base si oui on l'ajoute dans les cat de l'aliment sinon
            cat_of_elm = cat_of_elm2.strip()
            try:
                cat_already_exist = Categorie.objects.get(nom=cat_of_elm)
                alm.categorie.add(cat_already_exist)

            except Categorie.DoesNotExist:
                new_cat = Categorie(nom=cat_of_elm)
                new_cat.save()
                alm.categorie.add(new_cat)
                nbr_cat = nbr_cat + 1
        alm.save()
        nbr_alm = nbr_alm + 1
        print("\n\n\n")
        print("{} aliments ajoutés, {} catégories ajouté\n".format(nbr_alm, nbr_cat))
