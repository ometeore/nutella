from django.db import models




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
        return self.salt_100g + self.acide_100g + self.sugar_100g + self.glucide_100g
    
    
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
                        candidates.append(al)
            if len(candidates) < 6:
                common_cat_numbers = common_cat_numbers - 1
                if common_cat_numbers == 0:
                    need_to_keep_looking = False
            else:
                need_to_keep_looking = False

        final_list = sorted(candidates, key=lambda aliment: aliment.sum_nutrition(), reverse=False)

        return final_list[0:6]


class Categorie(models.Model):
    nom = models.CharField("nom", max_length=80, unique=True)

    def __str__(self):
        return self.nom
