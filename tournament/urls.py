from django.urls import path
from .views import *

app_name = 'tournament'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload_replay/', ReplayFormView.as_view(), name='upload_replay'),
    path('replay_list/', ReplayListView.as_view(), name='replay_list'),
    path('download_replay/<path:file_path>/', ReplayDownload.as_view(), name='download_replay'),
    path('tournament_list', TournamentListView.as_view(), name='tournament_list'),
    path('tournament/<int:pk>', TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournament/<int:pk>/enter_tournament/', enter_tournament, name='enter_tournament'),
    path('tournament/<int:pk>/leave_tournament/', leave_tournament, name='leave_tournament'),
]