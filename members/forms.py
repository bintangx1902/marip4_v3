from django import forms
from .models import UserProfile


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'phone', 'profile_image', 'about_me')
