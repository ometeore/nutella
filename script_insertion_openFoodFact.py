import json
import requests
from aliment.models import Aliment


class API:
    """ """

    def insertion(self, categorie):
        """ return list of request ready to apply """
        url_before_categorie = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0="
        url_after_categorie = "legumes&sort_by=unique_scans_n&page_size=1&axis_x=energy&axis_y=products_n&action=display&json=1"
        url = url_before_categorie + categorie + url_after_categorie
        encoded = requests.get(url).json()
        # payload = {'action': 'process', 'key2': 'value2'}
        # r = requests.get('https://httpbin.org/get', params=payload)
        products = self.encoded["products"]  # <-- list

        for product in products:
            print(product["product_name_fr"])
        # name_of_product = []
        # nutrition_grade_of_product = []
        # location_of_product = []
        # url_of_product = []
        # list_of_request = []


#
# for product in products:
#    try:
#        name_of_product.append(product['product_name_fr'])  #<-- list de nom des produits
#    except:
#        name_of_product.append("NOOOOOOOON")
#    try:
#        location_of_product.append(product['stores'])
#    except:
#        location_of_product.append("non disponible")
#    url_of_product.append(product['url'])
#    nutrition_grade_of_product.append(product['nutrition_grades_tags'][0])
# i = 0
# id_of_aliment = 62
# for name in name_of_product:
#    list_of_request.append("INSERT INTO OCOFF_aliments VALUES ('{}','{}', '{}', '{}', 'vide pour le moment', '{}', '{}')".format(j, name, nutrition_grade_of_product[i], self.id_categorie, location_of_product[i], url_of_product[i]))
#    i = i + 1
#    j = j+1
#
# return list_of_request
