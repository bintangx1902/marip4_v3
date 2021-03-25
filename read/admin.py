from django.contrib import admin
from .models import Comment, HistoryRecord

admin.site.register(Comment)
admin.site.register(HistoryRecord)
