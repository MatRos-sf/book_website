from django.urls import path, include
from .views import HomeView, add_or_edit, url_import
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add/', add_or_edit, name='add'),
    path('edit/<int:id>/', add_or_edit, name='edit'),
    path('import/', url_import, name='import')
]