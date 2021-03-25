from django.db import models
from ckeditor.fields import RichTextField
from backend.models import Book
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comment', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = CKEditor5Field('Text', null=True, blank=True, config_name='special')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.book.title, self.name)


class HistoryRecord(models.Model):
    user = models.ForeignKey(User, related_name='user_history', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='booking', on_delete=models.CASCADE)
    url = models.TextField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " membaca " + str(self.book)
