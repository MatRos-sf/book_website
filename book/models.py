from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.fullname

class Book(models.Model):
    #Zamodeluj obiekty bazodanowe tak by zawierały pola: tytuł, autor, data , numer ISBN, liczba stron, link do okładki i język .
    title = models.CharField(max_length=150, blank=False)
    authors = models.ManyToManyField(Author)
    publishedDate = models.IntegerField()
    ISBN = models.CharField(max_length=50)
    pageCount = models.IntegerField(default=0)
    previewLink = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, default='PL')         #trochę na sztywno !!!!
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


