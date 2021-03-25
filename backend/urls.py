from django.urls import path
from .views import *

app_name = 'my'

urlpatterns = [
    path('', redirect_check, name='redirect'),
    path('book/', BookListUploaded.as_view(), name='book-list'),
    path('book/check/', upload_check, name='book-check'),
    path('book/upload/', UploadBook.as_view(), name='upload-a-book'),
    path('book/<slug:link>/', BookDetail.as_view(), name='book-detail'),
    path('book/<slug:link>/update', UpdateBook.as_view(), name='book-update'),
    path('book/<slug:link>/delete/', BookDelete.as_view(), name='book-delete'),
]
