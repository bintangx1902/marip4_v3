from django import forms
from .models import Book, Category

category_choices = Category.objects.all().values_list("id", "name")

category_list = []

for category in category_choices:
    category_list.append(category)


class UploadBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'book', 'cover', 'author', 'availability', 'description', 'category')

        widgets = {
            'category': forms.CheckboxSelectMultiple(choices=category_list)
        }


class UpdateUploadedBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'availability', 'description', 'category')

        widgets = {
            'category': forms.CheckboxSelectMultiple(choices=category_list)
        }
