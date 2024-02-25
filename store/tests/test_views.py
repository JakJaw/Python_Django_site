from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product
import json


class TestViews(TestCase):
    
    def tests_project_search_GET(self):
        client = Client
        
        response = client.get(reverse('store'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')