from django.test import TestCase, Client
from django.urls import reverse
from book.views import HomeView
from book.models import Book, Author

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_one = Author.objects.create(fullname='TestOne')
        self.author_two = Author.objects.create(fullname='TestTwo')
        self.book_one = Book.objects.create(title="BookTest", publishedDate= 1995,
                                            ISBN= '123456789', pageCount= 123,
                                            previewLink= 'https://www.djangoproject.com/',
                                            language='PL')
        self.book_one.authors.add(self.author_one)
        self.book_two = Book.objects.create(title="Testowanie", publishedDate= 2022,
                                            ISBN= '987654321', pageCount= 222,
                                            previewLink= 'https://www.djangoproject.com/download/',
                                            language='EN')
        self.book_two.authors.add(self.author_two)

    def test_home_views_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'book/home_page.html')

    def test_home_views_get_search_value(self):
        response = self.client.get(reverse('home'), {'q': 'PL', 'from_to': ''})
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_home_views_get_search_value_date(self):
        response = self.client.get(reverse('home'), {'q': '', 'from_to': '2022'})
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_edit_view_post(self):
        payload = {
            'title': "Nowy",
            'authors': 'TestOne',
            "publishedDate": 2010,
            "ISBN": '123456789',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        response = self.client.post(reverse('edit', args=[1]), payload)
        book_update = Book.objects.get(id=1)
        self.assertEqual(book_update.publishedDate, payload['publishedDate'])
        self.assertEqual(book_update.ISBN, payload['ISBN'])
        self.assertEqual(book_update.pageCount, payload['pageCount'])
        self.assertEqual(book_update.language, payload['language'])
        self.assertEqual(response.status_code,200)

    def test_edit_view_post_invalid(self):
        payload = {
            'title': "Nowy",
            "publishedDate": 2010,
            "ISBN": '12345678',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        response = self.client.post(reverse('edit', args=[1]), payload)
        book_update = Book.objects.get(id=1)
        self.assertNotEqual(book_update.publishedDate, payload['publishedDate'])
        self.assertNotEqual(book_update.ISBN, payload['ISBN'])
        self.assertNotEqual(book_update.pageCount, payload['pageCount'])
        self.assertNotEqual(book_update.language, payload['language'])
        self.assertEqual(response.status_code, 200)

    def test_add_view_post(self):
        payload = {
            'title': "Nowy",
            'authors': 'TestOne',
            "publishedDate": 2010,
            "ISBN": '123',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        response = self.client.post(reverse('add'), payload)
        self.assertEqual(Book.objects.count(), 3)

    def test_add_view_post_invalid_ISBN(self):
        payload = {
            'title': "Nowy",
            'authors': 'TestOne',
            "publishedDate": 2010,
            "ISBN": '123456789',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        response = self.client.post(reverse('add'), payload)
        #nie doda
        self.assertEqual(Book.objects.count(), 2)

class ImportTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_import_data_with_link(self):
        url = "https://www.googleapis.com/books/v1/volumes?q=Hobbit"
        response = self.client.post(reverse('import'), {'url': url})
        self.assertEqual(Book.objects.count(), 10)
        url = 'https://www.googleapis.com/books/v1/volumes?q=Encyklopedia'
        response = self.client.post(reverse('import'), {'url': url})
        self.assertEqual(Book.objects.count(), 20)

    def test_import_repeat_link(self):
        url = "https://www.googleapis.com/books/v1/volumes?q=Hobbit"
        response = self.client.post(reverse('import'), {'url': url})
        response_two = self.client.post(reverse('import'), {'url': url})
        self.assertEqual(Book.objects.count(), 10)





