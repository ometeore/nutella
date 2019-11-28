from django.test import TestCase
from aliment.models import Aliment, Categorie
#
#class AnimalTestCase(TestCase):
#    def setUp(self):
#        Animal.objects.create(name="lion", sound="roar")
#        Animal.objects.create(name="cat", sound="meow")
#
#    def test_animals_can_speak(self):
#        """Animals that can speak are correctly identified"""
#        lion = Animal.objects.get(name="lion")
#        cat = Animal.objects.get(name="cat")
#        self.assertEqual(lion.speak(), 'The lion says "roar"')
#        self.assertEqual(cat.speak(), 'The cat says "meow"')

class alimentTestCase(TestCase):
    def setUp(self):
        cat = Categorie.objects.create(nom="Fruit")
        Aliment.objects.create(nom="Pomme",note_nutritionelle="a",categorie=cat, url_off="http",url_img="http2",repere_nutritionel="http3")
