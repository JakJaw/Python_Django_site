from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import store, product_detail, search, filter_products, submit_review

class TestUrls(SimpleTestCase):
    
    def test_store_url_resolves(self):
        url = reverse('store')
        self.assertEqual(resolve(url).func, store)
