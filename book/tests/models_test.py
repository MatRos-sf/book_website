from django.test import TestCase
from book.models import Book, Author

class ModelsTest(TestCase):
    def test_moduls_Book(self):
        payload = {
            'title': "Oczy smoka",
            'authors': 'Stephen King',
            "publishedDate": 2022,
            "ISBN": '9788382159431',
            "pageCount": 222,
            "previewLink": "https://lubimyczytac.pl/ksiazka/5008504/oczy-smoka",
            "language": 'pl'
        }
        payload_nd = {
            'title': "Głęboka woda",
            'authors': 'Patricia Highsmith',
            "publishedDate": 2022,
            "ISBN": '9788373927605',
            "previewLink": "https://lubimyczytac.pl/ksiazka/4997595/gleboka-woda",
            "language": 'pl'
        }

        author_payload_first = payload.get('authors')
        author_payload_second = payload_nd.get('authors')
        a_one= Author.objects.create(fullname=author_payload_first)
        a_two = Author.objects.create(fullname=author_payload_second)

        payload.pop('authors')
        b_one = Book.objects.create(**payload)
        b_one.authors.add(a_one)
        b_one.save()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(b_one.title, "Oczy smoka")

        payload_nd.pop('authors')
        b_two = Book.objects.create(**payload_nd)
        b_two.authors.add(a_two)
        b_two.save()

        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)

