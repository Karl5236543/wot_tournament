from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, FileResponse
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required, permission_required
from .services.tournament import tournament_add_user, tournament_delete_user

class IndexView(TemplateView):
    template_name = 'tournament/index.html'


class ReplayFormView(FormView):
    template_name = 'tournament/upload_replay_form.html'
    form_class = ReplayForm
    success_url = reverse_lazy('tournament:index')
    
    def form_valid(self, form):
        uploaded_file = form.cleaned_data['replay']
        file_path = os.path.join(settings.REPLAYS_ROOT, uploaded_file.name)
        with open(file_path, 'wb') as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)
        return super().form_valid(form)

class ReplayListView(ListView):
    template_name = 'tournament/replay_list.html'
    context_object_name = 'replay_files_names'
    
    def get_replay_files_path(self):
        return [os.path.basename(file) for file in os.scandir(settings.REPLAYS_ROOT)]
        
    def get_queryset(self):
        return self.get_replay_files_path()
    
    
class ReplayDownload(View):
    def get(self, request, file_path):
        file_path = os.path.join(settings.REPLAYS_ROOT, file_path)
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    

class TournamentListView(ListView):
    model = Tournament
    paginate_by = 5
    
class TournamentDetailView(DetailView):
    model = Tournament
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_in_current_tournament'] = self.request.user in self.object.players.all()
            if not context['user_in_current_tournament']:
                context['user_in_othe_tournament'] = bool(self.request.user.tournaments.all().count())
        return context
    

@login_required
@permission_required('tournament.can_enter', raise_exception=True)
def enter_tournament(request, pk):
    tournament_add_user(request.user, pk)
    return redirect('tournament:tournament_detail', pk=pk)

@login_required
def leave_tournament(request, pk):
    tournament_delete_user(request.user, pk)
    return redirect('tournament:tournament_detail', pk=pk)
    
    

    
    
# class CreateTankView(CreateView):
#     model = Tank
#     fields = '__all__'
#     success_url = reverse_lazy('accounts:register_done')

