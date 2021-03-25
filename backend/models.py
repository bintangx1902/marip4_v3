from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    link = models.SlugField(max_length=255, unique=True, default='') # ng usah
    book = models.FileField(upload_to='book/pdf/') # ng usah
    cover = models.ImageField(upload_to='book/cover/')
    author = models.CharField(max_length=255)
    availability = models.IntegerField(default=0)
    description = CKEditor5Field(null=True, blank=True, config_name='special')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    pending = models.BooleanField(default=True) # ng usah
    upload_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    category = models.ManyToManyField(Category, blank=True)

    def ttl_like(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.book.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        links = self.link
        links = str(links)
        return reverse('read:detail', args=[links])
