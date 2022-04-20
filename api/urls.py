from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, AuthorView

app_name  = 'api'
router = DefaultRouter()
router.register(r'', BookViewSet, 'api_home')
router.register(r'author', AuthorView)


urlpatterns = [
    path('', include(router.urls)),
]