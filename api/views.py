from rest_framework import viewsets
from book.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import filters
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'ISBN','authors__fullname','pageCount', 'previewLink', 'language']

    def create(self, request, *args, **kwargs):
        book = Book.objects.create(
            title=request.data['title'],
            publishedDate=request.data['publishedDate'],
            ISBN=request.data['ISBN'],
            pageCount=request.data['pageCount'],
            previewLink=request.data['previewLink'],
            language=request.data.get('language','PL')

        )
        cd_authors = request.data.get('authors',None)
        if cd_authors:
            for author in cd_authors.split(','):
                try:
                    a = Author.objects.get(fullname=author)
                except:
                    a = Author.objects.create(fullname=author)
                book.authors.add(a)
        else:
            try:
                a = Author.objects.get(fullname='anonym')
            except:
                a = Author.objects.create(fullname='anonym')
            book.authors.add(a)
        #serializer = BookSerializer(book, many=False)
        return Response(status=201)
    def update(self, request, *args, **kwargs):
        book = self.get_object()
        book.title = request.data['title']
        book.ISBN = request.data['ISBN']
        book.publishedDate = request.data['publishedDate']
        book.previewLink = request.data['previewLink']
        book.language = request.data['language']
        book.pageCount = request.data['pageCount']

        if request.data.get('authors', None):
            authors = request.data['authors']
            authors = authors.split(',')
            # to_delete - zminenna która gromadzi autorów którzy mają zostać usunięci
            to_delete = []
            # pętla sprawdzająca czy poprzedni autorzy są w nowym formularzu
            for author in book.authors.all():
                if author.fullname not in authors:
                    to_delete.append(author)
                else:
                    authors.remove(author.fullname)
            # Autorzy do usunięcia
            if to_delete:
                for d in to_delete:
                    book.authors.remove(d)

            # Add new authors
            for author in authors:
                # get or create author
                try:
                    a = Author.objects.get(fullname=author)
                except:
                    a = Author.objects.create(fullname=author)

                book.authors.add(a.id)
        book.save()
        return Response(status=200)


class AuthorView(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


