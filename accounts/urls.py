from django.urls import path, include
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register_done/', RegisterDoneView.as_view(), name='register_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('users/', PlayerListView.as_view(), name='users'),
    path('dialog/create/<int:user_id>/', DialogCreateView.as_view(), name='create_dialog'),
    path('message/create/<int:dialog_id>/', MessageCreateView.as_view(), name='create_message'),
    path('', include('django.contrib.auth.urls')),
]