from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse

class IndexView(TemplateView):
    template_name = 'tournament/index.html'

