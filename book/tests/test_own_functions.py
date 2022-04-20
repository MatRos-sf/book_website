from book.views import search_date, add_book
from unittest import TestCase
from datetime import datetime
from book.models import Book


class OwnFunctionsSearchData(TestCase):
    def test_search_date_all_corect(self):
        from_to = '1990-2000'
        self.assertEqual(search_date(from_to), [1990,2000])
    def test_search_date_greater_less(self):
        from_to = '2000-1990'
        self.assertEqual(search_date(from_to), [1990, 2000])
    def test_search_date_greater_equal(self):
        from_to = '2000-2000'
        self.assertEqual(search_date(from_to), [2000,2000])
    def test_search_date_miss_one_arg_first(self):
        from_to = '-2000'
        self.assertEqual(search_date(from_to), [2000,datetime.now().year])
    def test_search_date_miss_one_arg_second(self):
        from_to = '2000'
        self.assertEqual(search_date(from_to), [2000,datetime.now().year])
    def test_search_date_miss_one_arg_third(self):
        from_to = '2000-'
        self.assertEqual(search_date(from_to), [2000,datetime.now().year])
    def test_search_date_miss_one_arg_fourth(self):
        from_to = '-'
        self.assertEqual(search_date(from_to), [datetime.now().year,datetime.now().year])

class OwnFunctionsAddBook(TestCase):
    def test_add_book_valid(self):
        payload = {
            "title": "Programowanie. Teoria i praktyka z wykorzystaniem C++. Wydanie III",
            "authors": ["Łukasz Piwko"],
            "publishedDate": "2020",
            "ISBN": [{'type': 'ISBN_10', 'identifier': '9788328363120'}],
            "pageCount": 1088,
            "previewLink": "https://lubimyczytac.pl/ksiazka/4930976/programowanie-teoria-i-praktyka-z-wykorzystaniem-c-wydanie-iii",
            "language": "pl"
        }
        book = add_book(**payload)
        self.assertEqual(book, 1)
        self.assertEqual(Book.objects.count(), 1)



