from django import forms
from .models import Book
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class AddOrEdit(forms.ModelForm):

    title = forms.CharField(error_messages={'required': "Write title book."},
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    authors = forms.CharField(error_messages={'required': "Write authors book."},
                              widget=forms.TextInput( attrs={'class': 'form-control',
                                                          'placeholder': 'Authors e.g Adam Mickiewicz, Juliusz Słowacki'}))
    previewLink = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Link Page'}))
    ISBN = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}))
    pageCount = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Page Count'}))
    publishedDate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Publish year'}))
    language = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Language'}))
    class Meta:
        model = Book
        fields = ["title", "authors", "publishedDate", "ISBN", "pageCount", "previewLink", "language"]

    def clean(self):
        cd = super().clean()
        # chceck link
        cd_url = cd.get('previewLink')
        val_url = URLValidator()
        try:
            val_url(cd_url)
        except ValidationError:
            raise forms.ValidationError('previewLink: Your link is wrong')

        #check page
        cd_pageCount = cd.get("pageCount")
        if not cd_pageCount.isnumeric():
            raise forms.ValidationError('pageCount: Your book need number of page!')

        #publishedDate


class URLImportForms(forms.Form):
    url = forms.CharField()

    def clean(self):
        cd = super().clean()
        cd_url = cd.get('url')
        if 'https://www.googleapis.com/books/' not in cd_url:
            raise forms.ValidationError('Something is wrong. Do you use googleapis.com ?')

