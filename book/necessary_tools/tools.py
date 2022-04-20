"""
W tym pliku znajdują się niezbędnę funkcje które ułatwiają funkcjonalność.
Nie umieściłem je w views gdyż chciałem aby było bardziej przejrzyście
"""
from datetime import datetime

from book.models import Book, Author


def search_date(from_to):
    """
    funkcja, która:
    -ustawia datę od najmniejszej do największej,
    -sprawdza poprawność
    -jeżeli nie zostały wpisane liczby zwraca []
    :param from_to: łańcuch znaków z datami przedzielone '-'
    :return: posortowana 2 elementowa tablica od min do max
    """
    if '-' not in from_to:
        try:
            a = int(from_to)
            b = datetime.now().year
        except:
            return []
    else:
        try:
            a, b = [int(i) for i in from_to.split('-')]
        except:
            a, b = from_to.split('-')
            if a.isnumeric():
                a = int(a)
            else:
                a = datetime.now().year
            if b.isnumeric():
                b = int(b)
            else:
                b = datetime.now().year

    return sorted([a, b])


def add_book(title, authors, publishedDate, ISBN, pageCount, previewLink, language):

    """
    Funkcja ta:
    -sprawdza wartości zmiennych a następnie jeżeli prawidłowe tworzy nowey obiekt Book i Author
    return: 0 nie dodano książki, 1 dodano książkę
    """
    # ISBN składa się z 13 cyfr ale zauważyłem, że nie raz podawane są jakieś przedrostki
    valid_isbn = ''
    for i in ISBN:
        if i.get('identifier'):
            number = i.get('identifier')
            if len(number) >= 13:
                valid_isbn = number
                break
    # date
    publishedDate = max([int(i) for i in publishedDate.split('-')])

    # domyślnie gdy nie ma podanej liczby stron będzie 0
    if not pageCount:
        pageCount = 0
    try:
        if Book.objects.get(ISBN=valid_isbn):
            print('W bazie znajduje się: ', title)
            return 0
    except:
        book = Book.objects.create(title=title, publishedDate=publishedDate, ISBN=valid_isbn,
                                   pageCount=pageCount, previewLink=previewLink, language=language)
        if authors:
            for author in authors:
                # get or create autors
                try:
                    a = Author.objects.get(fullname=author)
                except:
                    a = Author.objects.create(fullname=author)
                book.authors.add(a.id)
        else:
            # When author is empty
            try:
                a = Author.objects.get(fullname='anonym')
            except:
                a = Author.objects.create(fullname='anonym')
            book.authors.add(a.id)
        book.save()
        return 1
