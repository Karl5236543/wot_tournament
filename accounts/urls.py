from django.urls import path, include
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_done/', RegisterDoneView.as_view(), name='register_done'),
    path('profile/', ProfileView.as_view(), name='profile')
]