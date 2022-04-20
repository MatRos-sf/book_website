from django.contrib import admin
from .models import Book, Author

@admin.register(Author)
class AuthorClass(admin.ModelAdmin):
    model = Author



@admin.register(Book)
class BookClass(admin.ModelAdmin):
    model = Book

