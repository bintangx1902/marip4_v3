from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField('Foto Profil Kamu(*opsional)', upload_to='profile/img/', null=True, blank=True)
    name = models.CharField('Nama yang akan kamu daftarkan (Wajib)', max_length=255, null=True)
    phone = models.CharField('Daftarkan Nomor WhatsApp Kamu dengan contoh 813xxxxxxxx', max_length=255, null=True)
    date_created = models.DateTimeField( auto_now_add=True, null=True)
    about_me = CKEditor5Field('Bagikan cerita tentang kamu (*Wajib) walau hanya singkat', config_name='special', default='')

    def __str__(self):
        return str(self.user) + ' as ' + self.name
