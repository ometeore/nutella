from django.test import TestCase, Client
from aliment.models import Aliment, Categorie
from utilisateur.models import MyUser


class TestAliment(TestCase):
    def setUp(self):
        cat1 = Categorie.objects.create(nom="Fruit")
        cat2 = Categorie.objects.create(nom="Steak")


        # la bannane a plus de glucide que la pomme
        self.Banane = Aliment.objects.create(nom="Banane",note_nutritionelle="a", url_off="http",url_img="http2", glucide_100g="12",salt_100g="1", sugar_100g="1", acide_100g="1")
        self.Banane.categorie.add(cat1)
        self.Pomme = Aliment.objects.create(nom="Pomme",note_nutritionelle="a", url_off="http",url_img="http2", glucide_100g="1",salt_100g="1", sugar_100g="1", acide_100g="1")
        self.Pomme.categorie.add(cat1)
        self.Poire = Aliment.objects.create(nom="Poire",note_nutritionelle="b", url_off="http",url_img="http2", glucide_100g="0.123",salt_100g="0.123", sugar_100g="0.123", acide_100g="0.123")
        self.Poire.categorie.add(cat1)
        self.Tournedos = Aliment.objects.create(nom="Tournedos",note_nutritionelle="unknown", url_off="http",url_img="http2", glucide_100g="0.123",salt_100g="0.123", sugar_100g="0.123", acide_100g="0.123")
        self.Tournedos.categorie.add(cat2)


    def test_aliment_substitution(self):
        ### Test l'algorithme de substitution ###
        self.assertEqual(self.Pomme.substitute(), [self.Banane])
        self.assertEqual(self.Poire.substitute(), [self.Pomme, self.Banane])

    def test_is_completed(self):
        self.assertEqual(self.Tournedos.is_complete(), False)
        self.assertEqual(self.Poire.is_complete(), True)


class TestStatus(TestCase):
    def setUp(self):
        
        self.user = MyUser.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        
        cat1 = Categorie.objects.create(nom="Fruit")
        self.Pomme = Aliment.objects.create(nom="Pomme",note_nutritionelle="a", url_off="http",url_img="http2", glucide_100g="0.123",salt_100g="0.123", sugar_100g="0.123", acide_100g="0.123")
        self.Pomme.categorie.add(cat1)

    def test_home(self):
        ### Test qu'on a bien une reponse en demandant l'accueil ###
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_connect_user(self):
        ### Test la connection d'un utilisateur ###
        response = self.client.post('/user/', {'identifiant': 'jacob', 'password': 'top_secret'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_disconect_user(self):
        ### test qu'au click sur disconect le user est logout ###
        pass

    def test_create_user(self):
        ### test le resultat de la création d'un utilisateur ###
        pass


    def test_search(self):
        #### Test le resultat d'une recherche depuis / d'un aliment 
        #### l'input est sur '/' le post pointe vers '/aliment/recherche'
        ####la recherche est un name contains
        pass

    def test_aliment_view(self):
        ###
        ### Cet aliment contient un js hide show
        ### 
        pass


#       access loged user
#       >>> c = Client()
#       >>> c.login(username='fred', password='secret')
#c = Client()
#>>> response = c.post('/login/', {'username': 'john', 'password': 'smith'})
#>>> response.status_code
#       
# 
# 
# class Response¶
#
#    client¶
#
#        The test client that was used to make the request that resulted in the response.
#
#    content¶
#
#        The body of the response, as a bytestring. This is the final page content as rendered by the view, or any error message.
#
#    context¶
#
#        The template Context instance that was used to render the template that produced the response content.
#
#        If the rendered page used multiple templates, then context will be a list of Context objects, in the order in which they were rendered.
#
#        Regardless of the number of templates used during rendering, you can retrieve context values using the [] operator. For example, the context variable name could be retrieved using:
#
#        >>> response = client.get('/foo/')
#        >>> response.context['name']
#        'Arthur'
#
#        Not using Django templates?
#
#        This attribute is only populated when using the DjangoTemplates backend. If you’re using another template engine, context_data may be a suitable alternative on responses with that attribute.
#
#    json(**kwargs)¶
#
#        The body of the response, parsed as JSON. Extra keyword arguments are passed to json.loads(). For example:
#
#        >>> response = client.get('/foo/')
#        >>> response.json()['name']
#        'Arthur'
#
#        If the Content-Type header is not "application/json", then a ValueError will be raised when trying to parse the response.
#
#    request¶
#
#        The request data that stimulated the response.
#
#    wsgi_request¶
#
#        The WSGIRequest instance generated by the test handler that generated the response.
#
#    status_code¶
#
#        The HTTP status of the response, as an integer. For a full list of defined codes, see the IANA status code registry.
#
#    templates¶
#
#        A list of Template instances used to render the final content, in the order they were rendered. For each template in the list, use template.name to get the template’s file name, if the template was loaded from a file. (The name is a string such as 'admin/index.html'.)
#
#        Not using Django templates?
#
#        This attribute is only populated when using the DjangoTemplates backend. If you’re using another template engine, template_name may be a suitable alternative if you only need the name of the template used for rendering.
#
#    resolver_match¶