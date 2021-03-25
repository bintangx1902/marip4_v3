from django import forms
from .models import *


class AddCommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
