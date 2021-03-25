from django.urls import path
from .views import *

app_name = 'read'

urlpatterns = [
    path('', AllBooksList.as_view(), name='book'),
    path('book/', AllBookList.as_view(), name='book-list'),
    path('maps/', maps_view, name='maps'),
    # path('<str:cats>/', CategorySearch, name='category'),
    path('<slug:link>/', BookDetailView.as_view(), name='detail'),
    path('<slug:link>/comment/', AddComment.as_view(), name='add-comment'),
    path('<str:link>/likes/', like_view, name='book-like'),
    path('<str:link>/view', insert_to_history, name='book-history'),
    path('<str:link>/view/', PdfView.as_view(), name='book-view'),
    path('<str:link>/profile/', ShowProfileUploaderProfile.as_view(), name='profile-view'),
]
