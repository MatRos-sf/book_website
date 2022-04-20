from rest_framework import serializers
from book.models import Book, Author



class BookSerializer(serializers.ModelSerializer):
    # authors = serializers.StringRelatedField(many=True)
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    class Meta:
        model = Book
        fields = ["title", "authors", "publishedDate", "ISBN", "pageCount", "previewLink", "language"]

class AuthorSerializer(serializers.ModelSerializer):
    book_list = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ("fullname", "book_list")


class BookDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    authors = serializers.CharField()
    publishedDate = serializers.CharField()
    ISBN = serializers.CharField()
    pageCount = serializers.CharField()
    previewLink = serializers.CharField()
    language = serializers.CharField()

