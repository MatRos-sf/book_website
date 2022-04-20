from django.test import SimpleTestCase
from django.urls import reverse, resolve
from book.views import HomeView, add_or_edit, url_import

class TestUrls(SimpleTestCase):

    def test_import_url_resolves(self):
        url = reverse('import')
        self.assertEqual(resolve(url).func, url_import)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func, add_or_edit)

    def test_edit_is_resolved(self):
        url = reverse('edit',args=[2])
        self.assertEqual(resolve(url).func, add_or_edit)



