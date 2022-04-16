# users/forms.py
from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Message, Player, Dialog

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Player
        fields = ('username', 'email', 'like_pancackes')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Player
        fields = ('username', 'email', 'like_pancackes')
        
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.view = kwargs.pop('view')
        super().__init__(*args, **kwargs)
              
    def save(self, *args, **kwargs):
        self.instance.sender = self.view.request.user
        self.instance.dialog = Dialog.objects.get(pk=self.view.kwargs['dialog_id'])
        return super().save(*args, **kwargs)
    