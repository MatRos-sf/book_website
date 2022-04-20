from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from book.models import Book

# Create your tests here.
class ApiTest(TestCase):
    def test_post(self):
        payload = {
            'title': "Nowy",
            'authors': 'TestOne, TestTwo',
            "publishedDate": 2010,
            "ISBN": '123456789',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        client = APIClient()
        response = client.post('http://127.0.0.1:8000/api/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
    def test_update(self):
        payload = {
            'title': "Nowy",
            'authors': 'TestOne, TestTwo',
            "publishedDate": 2010,
            "ISBN": '123456789',
            "pageCount": 202,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        client = APIClient()
        response = client.post('http://127.0.0.1:8000/api/', payload, format='json')
        payload = {
            'title': "nowy",
            'authors': "Nowy",
            "publishedDate": 2010,
            "ISBN": '123456789',
            "pageCount": 2002,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'en'
        }
        response = client.put('http://127.0.0.1:8000/api/1/', payload, format='json')
        b=Book.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b.title, 'nowy')
        self.assertEqual(b.pageCount, 2002)



