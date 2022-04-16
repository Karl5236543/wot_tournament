from dis import dis
from pyexpat import model
from re import template
from tkinter import dialog
from urllib import request
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView, View, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from tournament.models import TournamentRecord
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.db.models import *
from django.db.models import *
from django.db.models import functions
from tournament.models import Tournament, Tank

User = get_user_model()

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')
    template_name = 'registration/register_form.html'


class RegisterDoneView(TemplateView):
    title = 'вы зарешистрированы'
    
    def get_title(self):
        """
        return title, that will be printed in template
        """
        return self.title
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
    
    template_name = 'registration/register_done.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
    
    
class UserUpdateView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/user_update_form.html'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    
class UserView(LoginRequiredMixin, DetailView):
    model=User
    
    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_active=True)
    
    
# class MessageCreateView(LoginRequiredMixin, CreateView):
#     success_url = reverse_lazy('tournament:index')
#     form_class = MessageForm
#     model = Message
    
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['request'] = self.request
#         return kwargs


class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    
    
class DialogCreateView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        
        tr = Tournament.objects.values("total_prize").annotate(total_count=Count("id"))
        print(tr)
        
                        
        dialogs = Dialog.objects.filter(users__pk=user_id).filter(users=self.request.user)
        if dialogs.exists():
            dialog = dialogs.first()
        else:
            dialog = Dialog.objects.create()
            dialog.users.add(
                request.user,
                Player.objects.get(pk=user_id),
            )
            dialog.save()
        url = reverse_lazy('create_message', kwargs={'dialog_id': dialog.pk})
        return HttpResponseRedirect(url)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    
    def get_success_url(self):
        return reverse_lazy('create_message', kwargs={'dialog_id': self.kwargs['dialog_id']})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['view'] = self
        return kwargs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['messages'] = Dialog.objects.get(pk=self.kwargs['dialog_id']).messages.order_by('time_created')
        return context