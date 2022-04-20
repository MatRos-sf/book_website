import json
from urllib import request as r

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import AddOrEdit, URLImportForms
from .models import Book, Author
from .necessary_tools.tools import search_date, add_book


class HomeView(ListView):
    model = Book
    template_name = 'book/home_page.html'
    context_object_name = 'books'

    def get_queryset(self):
        query_q = self.request.GET.get('q')
        query_f_t = self.request.GET.get('from_to')
        object_list = []
        if query_q:
            # szukanie po tytuł, autor, numer ISBN, liczba stron, link , język
            object_list = self.model.objects.filter(
                Q(title__icontains=query_q) | Q(authors__fullname__icontains=query_q) |
                Q(ISBN__icontains=query_q) | Q(language__icontains=query_q) |
                Q(pageCount__icontains=query_q) | Q(previewLink__icontains=query_q))
            object_list = object_list.distinct()
        # szukanie po dacie publikacji
        if query_f_t:
            query_f_t = search_date(query_f_t)
            if object_list:
                if query_f_t:
                    object_list = object_list.filter(Q(publishedDate__gte=query_f_t[0]),
                                                     Q(publishedDate__lte=query_f_t[1]))
            else:
                if query_f_t:
                    object_list = self.model.objects.filter(Q(publishedDate__gte=query_f_t[0]),
                                                            Q(publishedDate__lte=query_f_t[1]))
        if not query_q and not query_f_t:
            object_list = self.model.objects.all()
        return object_list


# add or edit
def add_or_edit(request, id=None):
    forms = AddOrEdit()
    info = []
    # edit
    if id:
        book = get_object_or_404(Book, pk=id)
        forms = AddOrEdit()
        if request.method == 'POST':
            forms = AddOrEdit(request.POST)
            if forms.is_valid():
                cd = forms.cleaned_data
                authors = cd.pop('authors')
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

                # Check another fields
                if book.title != cd['title']:
                    book.title = cd['title']
                    info.append('Title')
                if book.publishedDate != int(cd['publishedDate']):
                    book.publishedDate = cd['publishedDate']
                    info.append('Publish year')
                if book.ISBN != cd['ISBN']:
                    book.ISBN = cd['ISBN']
                    info.append('ISBN')
                if book.previewLink != cd['previewLink']:
                    book.previewLink = cd['previewLink']
                    info.append('Link')
                if book.language != cd['language']:
                    book.language = cd['language']
                    info.append('Language')
                if book.pageCount != int(cd['pageCount']):
                    book.pageCount = cd['pageCount']
                    info.append('Page ')
                book.save()
                return render(request, "book/add_or_edit.html", {"forms": forms, "edit": True,
                                                                 'detail_book': book, 'info': info})

        return render(request, "book/add_or_edit.html", {"forms": forms,
                                                         "edit": True,
                                                         'detail_book': book,
                                                         'info': info})

    else:
        if request.method == 'POST':
            forms = AddOrEdit(request.POST)
            if forms.is_valid():
                # dodanie autorów
                cd = forms.cleaned_data
                authors = cd.pop('authors')
                try:
                    if Book.objects.get(ISBN=cd['ISBN']):
                        return render(request, 'book/add_or_edit.html', {"forms": forms,
                                                                         "edit": False,
                                                                         'info_error': 'Exist object with this ISBN'})
                except:
                    book = Book.objects.create(**cd)

                    for author in authors.split(','):
                        # get or create autors
                        try:
                            a = Author.objects.get(fullname=author)
                        except:
                            a = Author.objects.create(fullname=author)
                        book.authors.add(a.id)
                    info.append('Book: ' + book.title)
                    book.save()

                    return render(request, 'book/add_or_edit.html', {"forms": forms,
                                                                     "edit": False,
                                                                     'detail_book': book,
                                                                     'info': info})
            else:
                print("Something wrong")
                return render(request, 'book/add_or_edit.html', {"forms": forms,
                                                                 "edit": False,
                                                                 'info': info})
    return render(request, "book/add_or_edit.html", {"forms": forms})


def url_import(request):

    forms = URLImportForms()
    amount_new_book = 0
    if request.method == "POST":
        forms = URLImportForms(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            url = cd['url']
            response = r.urlopen(url)
            items = json.load(response)['items']
            for item in items:
                a = item["volumeInfo"]
                title = a.get("title")
                authors = a.get("authors")
                publishedDate = a.get("publishedDate")
                ISBN = a.get("industryIdentifiers")
                pageCount = a.get("pageCount")
                previewLink = a.get("previewLink")
                language = a.get("language")
                amount_new_book += add_book(title, authors, publishedDate, ISBN, pageCount, previewLink, language)

    return render(request, 'book/import.html', {'forms': forms,
                                                'amount_new_book': amount_new_book})
