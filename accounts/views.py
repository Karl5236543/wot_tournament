from re import template
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:register_done')
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