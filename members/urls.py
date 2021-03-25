from django.urls import path
from .views import *

app_name = 'profile'

urlpatterns = [
    path('', ProfileHome.as_view(), name='home'),
    # path('', profile_home, name='home'),
    path('check/', profile_ck, name='cek-profile'),
    path('create/', CreateProfile.as_view(), name='create-profile'),
    path('<str:pk>/update/', UpdateProfile.as_view(), name='update-profile'),
]
