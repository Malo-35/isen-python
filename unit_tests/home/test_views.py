from django.urls import reverse 
from django.test import Client, RequestFactory, TestCase
from pytest_django.asserts import assertTemplateUsed
import pytest

from home.views import RedirectHomeView, HomeView
from products.models import Product


def test_RedirectHomeView():
    client = Client()
    response = client.get(reverse('redirect_home'))

    """ 
    Testing if our RedirectHomeView redirects succuessfully (status_code 302)
    For the second assert, We are testing if we redirect to the '/home/' url
     """

    assert response.status_code == 302
    assert response.url == '/home/'

@pytest.mark.django_db
def test_HomeView():
    client = Client()
    response = client.get(reverse('home'))

    """ 
    In the first assert, We are testing if our get request returns 200 (OK) status code 
    For the second assert, we are making sure that our view returns the home.html template
    """
    
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

class HomeViewTestCase(TestCase):
    def setUp(self):
        # Crée un ensemble de produits
        Product.objects.create(name='Produit A', price=10.00, description="Desc", image="img.png")
        Product.objects.create(name='Produit B', price=20.00, description="Desc", image="img.png")
        Product.objects.create(name='Produit C', price=15.00, description="Desc", image="img.png")

        self.factory = RequestFactory()

    def test_get_queryset_default_order(self):
        request = self.factory.get('/home/')
        view = HomeView()
        view.request = request

        queryset = view.get_queryset()
        prices = list(queryset.values_list('price', flat=True))
        # Aucun tri appliqué, donc dépend de l'ordre d'insertion
        self.assertEqual(len(prices), 3)

    def test_get_queryset_price_asc(self):
        request = self.factory.get('/home/?sort=price_asc')
        view = HomeView()
        view.request = request

        queryset = view.get_queryset()
        prices = list(queryset.values_list('price', flat=True))
        self.assertEqual(prices, sorted(prices))

    def test_get_queryset_price_desc(self):
        request = self.factory.get('/home/?sort=price_desc')
        view = HomeView()
        view.request = request

        queryset = view.get_queryset()
        prices = list(queryset.values_list('price', flat=True))
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_get_queryset_invalid_sort(self):
        request = self.factory.get('/home/?sort=invalid')
        view = HomeView()
        view.request = request

        queryset = view.get_queryset()
        prices = list(queryset.values_list('price', flat=True))
        # Devrait ne pas trier, donc on vérifie juste que les éléments sont là
        self.assertEqual(len(prices), 3)